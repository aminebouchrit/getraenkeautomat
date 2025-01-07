""" SWTP_Ebner_WiSe23_Getraenkemaschine
Handler for queries related to orders

Version 0.1
Licence: MIT
"""

import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database.model import (
    Bottle, BottleItem, Recipe, Order, OrderStatus, OrderItem, Glass, Machine
)

class OrderHandler:
    def __init__(self, engine, util_handler, frontend_publisher, machine_publisher):
        self.engine = engine
        self.util_handler = util_handler

        # used for sending info and error messages to the client
        self.frontend_publisher = frontend_publisher

        # used for sending config and order messages to the machine
        self.machine_publisher = machine_publisher

    # ---- frontend-facing queries ----

    def create_order(self, input_data, client_id):
        # extract input data
        machine_id = input_data["machineID"]
        recipe_id = input_data["recipeID"]

        with Session(self.engine) as session:
            # check if the machine exists
            machine = session.get(Machine, machine_id)
            if machine is None:
                return False, "Machine does not exist"

            # get recipe that is used by the order
            recipe = session.get(Recipe, recipe_id)
            if recipe is None:
                return False, "Recipe does not exist"

            # create order object
            new_order = Order(start_time=func.now(), last_update=func.now(), status=OrderStatus.waiting,
                              client_id=client_id, recipe_id=recipe_id, glass_id=recipe.glass_id, machine_id=machine_id)

            # add order entries according to the recipe
            for recipe_item in recipe.recipe_items:
                # find a bottle that matches the item category and is available
                matching_bottle = self.util_handler.get_matching_bottle(recipe_item.category_id, recipe_item.amount_ml, True, machine_id)

                if matching_bottle is None:
                    # no matching bottle was found
                    return False, "Bottles are missing or do not have enough capacity left"

                # create order item
                order_item = OrderItem(amount_ml=recipe_item.amount_ml, bottle_id=matching_bottle.id)
                new_order.order_items.append(order_item)

                # find bottle item that corresponds to the selected bottle
                item_query = select(BottleItem).filter_by(bottle_id=matching_bottle.id, machine_id=machine_id)
                item_query = item_query.where(BottleItem.current_capacity >= order_item.amount_ml)
                bottle_item = session.scalars(item_query).first()

                # adjust capacity of the bottle item
                bottle_item.current_capacity -= recipe_item.amount_ml

            # add order to the database
            session.add(new_order)

            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                return False, f"Error creating order: {e}"

        # start order if no other is in progress
        self.start_next_order(machine_id)

        return True, "Order created successfully"

    def create_customorder(self, input_data, client_id):
        # extract input data
        machine_id = input_data["machineID"]
        recipe_items = input_data["value"]

        with Session(self.engine) as session:
            # check if the machine exists
            machine = session.get(Machine, machine_id)
            if machine is None:
                return False, "Machine does not exist"

            # find a glass that best fits the order
            sum_amount = sum([recipe_item["amount_ml"] for recipe_item in recipe_items])
            glass_query = select(Glass.id).where(Glass.amount_ml >= sum_amount)
            glass_query = glass_query.order_by(Glass.amount_ml)
            glass_id = session.scalars(glass_query).first()

            if glass_id is None:
                return False, "No fitting glass!"

            # create order object
            new_order = Order(start_time=func.now(), last_update=func.now(), status=OrderStatus.waiting,
                              client_id=client_id, glass_id=glass_id, machine_id=machine_id)

            # add order entries according to the input
            for recipe_item in recipe_items:
                order_item = OrderItem(amount_ml=recipe_item["amount_ml"], bottle_id=recipe_item["bottleID"])
                new_order.order_items.append(order_item)

                # find bottle item that corresponds to the selected bottle and whose capacity is still high enough
                item_query = select(BottleItem).filter_by(bottle_id=order_item.bottle_id, machine_id=machine_id)
                item_query = item_query.where(BottleItem.current_capacity >= order_item.amount_ml)
                bottle_item = session.scalars(item_query).first()

                if bottle_item is None:
                    # no matching bottle item was found
                    return False, "Bottles are missing or do not have enough capacity left"

                # adjust capacity of the bottle item
                bottle_item.current_capacity -= recipe_item["amount_ml"]

            # add order to the database
            session.add(new_order)

            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                return False, f"Error creating order: {e}"

        # start order if no other is in progress
        self.start_next_order(machine_id)

        return True, "Order created successfully"


    # ---- backend-facing queries ----

    def on_machine_info(self, machine_id, input_data):
        if input_data == 0:
            # order has been processed successfully
            self.send_to_orderer(machine_id, "info", "Order completed")
            self.change_pending_order_status(machine_id, OrderStatus.completed)
            self.start_next_order(machine_id)
        elif input_data == 1:
            # order restarted
            self.send_to_orderer(machine_id, "info", "Order continues after error")
            self.change_pending_order_status(machine_id, OrderStatus.pending) # keep status, but mark as updated

    def on_machine_error(self, machine_id, input_data):
        error_code = input_data["error_code"]
        error_info = input_data["error_info"]

        if error_code == 0:
            # empty bottle
            self.send_to_orderer(machine_id, "error", f"Bottle at station {error_info} is unexpectedly empty, please contact a machine manager")
            self.change_pending_order_status(machine_id, OrderStatus.pending) # keep status, but mark as updated
        elif error_code == 1:
            # glass removed
            self.send_to_orderer(machine_id, "error", "Glass was removed during the order, please place it again and continue the order")
            self.change_pending_order_status(machine_id, OrderStatus.pending) # keep status, but mark as updated
        elif error_code == 2:
            # order cannot be processed (undefined station id)
            self.send_to_orderer(machine_id, "error", f"Order failed (station {error_info} is undefined)")
            self.change_pending_order_status(machine_id, OrderStatus.failed)
            self.start_next_order(machine_id)
        elif error_code == 3:
            # error code 3 belongs to the LED management and is currently not implemented
            pass
        elif error_code == 4:
            # configuration error
            self.send_to_orderer(machine_id, "error", "Configuration error, your order may not be processed properly")


    # ---- internal queries ----

    def start_next_order(self, machine_id):
        # check if there are old orders that have not been completed
        self.timeout_orders()

        # only start order if no other is active for the given machine
        if not self.is_order_in_progress(machine_id):
            with Session(self.engine) as session:
                # search for an order that is currently waiting to be processed
                sql_query = select(Order).filter_by(machine_id=machine_id, status=OrderStatus.waiting)
                sql_query = sql_query.order_by(Order.start_time) # process oldest order first
                waiting_order = session.scalars(sql_query).first()

                # check if there is an order that has not been processed
                if waiting_order is not None:
                    # trigger order
                    self.send_order_to_machine(waiting_order)

                    # update status
                    waiting_order.status = OrderStatus.pending
                    waiting_order.last_update = func.now() # mark order as updated
                    session.commit()

    def timeout_orders(self):
        with Session(self.engine) as session:
            # if there was no machine response in the last 15 minutes, an order is considered failed
            timeout_date = datetime.datetime.now() - datetime.timedelta(minutes=15)

            # set status of all orders that have timed out to 'failed'
            sql_query = select(Order).filter_by(status=OrderStatus.pending)
            sql_query = sql_query.where(Order.last_update < timeout_date)
            timed_out = session.scalars(sql_query)

            for order in timed_out:
                order.status = OrderStatus.failed

            session.commit()

    def is_order_in_progress(self, machine_id):
        with Session(self.engine) as session:
            # check if there is an order in progress (state: pending) for the given machine
            order_query = select(Order).filter_by(machine_id=machine_id, status=OrderStatus.pending)
            first_match = session.execute(order_query).first()

        if first_match is None:
            # no order is in progress
            return False
        else:
            return True

    def send_to_orderer(self, machine_id, message_type, message):
        with Session(self.engine) as session:
            # search for the order that is currently pending
            # (there can only be on pending order per machine)
            sql_query = select(Order).filter_by(machine_id=machine_id, status=OrderStatus.pending)
            pending_order = session.execute(sql_query).scalar_one_or_none()

            if pending_order is not None:
                # send message to the client that started the order
                self.frontend_publisher.send_to_client(pending_order.client_id, message_type, message)

    def change_pending_order_status(self, machine_id, new_status):
        with Session(self.engine) as session:
            # search for the order that is currently pending
            # (there can only be on pending order per machine)
            sql_query = select(Order).filter_by(machine_id=machine_id, status=OrderStatus.pending)
            pending_order = session.execute(sql_query).scalar_one_or_none()

            if pending_order is not None:
                # change order state
                pending_order.status = new_status

                # mark order as updated
                pending_order.last_update = func.now()

                session.commit()

    def send_order_to_machine(self, order):
        # send necessary station config
        self.machine_publisher.send_to_bridge(order.machine_id, self.get_station_config(order))

        # create stations that are part of the order
        stations = []

        with Session(self.engine) as session:
            for order_item in order.order_items:
                # convert amount from ml to gram
                bottle = session.get(Bottle, order_item.bottle_id)
                item_weight = order_item.amount_ml * bottle.density

                stations.append({
                    "stationID": self.get_station_id(order, order_item),
                    "value": int(item_weight)
                })

        # build order as JSON
        json_format = {
            "type": "order",
            "glass_weight": order.glass.weight_g,
            "value": stations
        }

        # send order to machine
        self.machine_publisher.send_to_bridge(order.machine_id, json_format)

    def get_station_config(self, order):
        stations = []

        with Session(self.engine) as session:
            # get list of stations
            bottle_query = select(BottleItem).join(Bottle).join(OrderItem)
            bottle_query = bottle_query.where(BottleItem.machine_id == order.machine_id)
            bottle_query = bottle_query.where(OrderItem.order_id == order.id)
            bottle_query = bottle_query.order_by(BottleItem.position_cm) # station ID is calculated according to the position of the bottle
            bottle_query = bottle_query.distinct() # prevent giving multiple ids to the same bottle item

            bottle_items = session.scalars(bottle_query)

            for idx, item in enumerate(bottle_items):
                station_item = {
                    "configID": 0, # bottle
                    "stationID": idx, # defined through order_by
                    "position": item.position_cm,
                    "pump_pin": item.pump_pin,
                    "led_pin": item.led_pin
                }
                stations.append(station_item)

        # build config as JSON
        json_format = {
            "type": "config",
            "value": stations
        }

        return json_format

    def get_station_id(self, order, order_item):
        with Session(self.engine) as session:
            # get list of stations
            bottle_query = select(BottleItem).join(Bottle).join(OrderItem)
            bottle_query = bottle_query.where(BottleItem.machine_id == order.machine_id)
            bottle_query = bottle_query.where(OrderItem.order_id == order.id)
            bottle_query = bottle_query.order_by(BottleItem.position_cm)  # station ID is calculated according to the position of the bottle
            bottle_query = bottle_query.distinct() # prevent giving multiple ids to the same bottle item

            bottle_items = session.scalars(bottle_query)

            for idx, item in enumerate(bottle_items):
                    if item.bottle_id == order_item.bottle_id:
                        # matching bottle item has been found -> return station ID
                        return idx
