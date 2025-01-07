""" SWTP_Ebner_WiSe23_Getraenkemaschine
Handler for update queries

Version 0.1
Licence: MIT
"""

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database.model import (
    Category, Bottle, BottleItem, Machine, Recipe, RecipeItem, Glass
)

class UpdateHandler:
    def __init__(self, engine):
        self.engine = engine

    def update_bottle(self, input_data, client_id):
        # extract input data
        bottle_id = input_data.get("bottleID")
        bottle_data = input_data.get("value", {})

        category_id = bottle_data.get("categoryID")
        name = bottle_data.get("name")
        density = bottle_data.get("density")
        max_capacity = bottle_data.get("max_capacity")
        alcohol_percentage = bottle_data.get("alcohol_percentage")
        price = bottle_data.get("price")
        pic_url = bottle_data.get("pic_url")

        with Session(self.engine) as session:
            # check if bottle exists
            bottle = session.get(Bottle, bottle_id)
            if bottle is None:
                return False, "Bottle does not exist"

            # update bottle attributes
            if category_id is not None:
                # check if category exists
                category = session.get(Category, category_id)
                if category is None:
                    return False, "Category does not exist"

                bottle.category_id = category_id
            if name is not None:
                bottle.name = name
            if density is not None:
                bottle.density = density
            if max_capacity is not None:
                bottle.max_capacity = max_capacity
            if alcohol_percentage is not None:
                bottle.alcohol_percentage = alcohol_percentage
            if price is not None:
                bottle.price = price
            if pic_url is not None:
                bottle.pic_url = pic_url

            # save changes
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                return False, f"Error updating bottle: {e}"

        return True, "Bottle updated successfully"

    def update_machine(self, input_data, client_id):
        # extract input data
        machine_data = input_data.get("value", {})
        machine_id = input_data.get("machineID")

        name = machine_data.get("name")
        bottle_items = machine_data.get("bottle_items", [])

        with Session(self.engine) as session:
            # check if machine exists
            machine = session.get(Machine, machine_id)
            if machine is None:
                return False, "Machine does not exist"

            # update machine attributes
            if name is not None:
                machine.name = name

            # update bottle items
            for bottle_item in bottle_items:
                position_cm = bottle_item.get("position_cm")
                pump_pin = bottle_item.get("pump_pin")
                led_pin = bottle_item.get("led_pin")
                current_capacity = bottle_item.get("current_capacity")
                bottle_id = bottle_item.get("bottleID")

                if bottle_id is not None:
                    # check if bottle exists
                    bottle = session.get(Bottle, bottle_id)
                    if bottle is None:
                        return False, f"Bottle {bottle_id} does not exist"

                # check if bottle item exists
                # (identify by position)
                bottle_item_db = session.scalars(select(BottleItem).filter_by(machine_id=machine_id, position_cm=position_cm)).first()
                if bottle_item_db is None:
                    # bottle item does not exist, so create a new one
                    # (all attributes are required in that case)
                    if pump_pin is None or led_pin is None or current_capacity is None or bottle_id is None:
                        return False, "All attributes are required when adding a new bottle item"

                    bottle_item_db = BottleItem(
                        machine_id=machine_id,
                        position_cm=position_cm,
                        pump_pin=pump_pin,
                        led_pin=led_pin,
                        current_capacity=current_capacity,
                        bottle_id=bottle_id
                    )
                    machine.bottle_items.append(bottle_item_db)
                else:
                    # bottle item exists, update bottle item attributes
                    if pump_pin is not None:
                        bottle_item_db.pump_pin = pump_pin
                    if led_pin is not None:
                        bottle_item_db.led_pin = led_pin
                    if current_capacity is not None:
                        bottle_item_db.current_capacity = current_capacity
                    if bottle_id is not None:
                        bottle_item_db.bottle_id = bottle_id

            # save changes
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                return False, f"Error updating machine: {e}"

        return True, "Machine updated successfully"

    def update_category(self, input_data, client_id):
        # extract input data
        category_id = input_data.get("categoryID")
        category_data = input_data.get("value", {})

        parent_id = category_data.get("parent_categoryID")
        name = category_data.get("name")

        with Session(self.engine) as session:
            # check if category exists
            category = session.get(Category, category_id)
            if category is None:
                return False, "Category does not exist"

            # update category attributes
            if "parent_categoryID" in category_data:
                # if the parent id is 'None', the parent relation is removed
                if parent_id is not None:
                    # otherwise, check if parent category exists
                    parent_category = session.get(Category, parent_id)
                    if parent_category is None:
                        return False, "Parent category does not exist"

                category.parent_id = parent_id
            if name is not None:
                category.name = name

            # save changes
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                return False, f"Error updating category: {e}"

        return True, "Category updated successfully"

    def update_recipe(self, input_data, client_id):
        # extract input data
        recipe_data = input_data.get("value", {})
        recipe_id = input_data.get("recipeID")

        name = recipe_data.get("name")
        price = recipe_data.get("price")
        pic_url = recipe_data.get("pic_url")
        category_id = recipe_data.get("categoryID")
        glass_id = recipe_data.get("glassID")
        recipe_items = recipe_data.get("recipe_items", [])

        with Session(self.engine) as session:
            # check if recipe exists
            recipe = session.get(Recipe, recipe_id)
            if recipe is None:
                return False, "Recipe does not exist"

            # update recipe attributes
            if name is not None:
                recipe.name = name
            if price is not None:
                recipe.price = price
            if pic_url is not None:
                recipe.pic_url = pic_url
            if category_id is not None:
                # check if bottle exists
                category = session.get(Category, category_id)
                if category is None:
                    return False, "Category does not exist"
                recipe.category_id = category_id
            if glass_id is not None:
                # check if glass exists
                glass = session.get(Glass, glass_id)
                if glass is None:
                    return False, "Glass does not exist"
                recipe.glass_id = glass_id

            # update recipe items
            for recipe_item in recipe_items:
                category_id = recipe_item.get("categoryID")
                amount_ml = recipe_item.get("amount_ml")

                # check if category exists
                category = session.get(Category, category_id)
                if category is None:
                    return False, f"Category {category_id} does not exist"

                # check if recipe item exists
                recipe_item_db = session.scalars(select(RecipeItem).filter_by(recipe_id=recipe_id, category_id=category_id)).first()
                if recipe_item_db is None:
                    # recipe item does not exist, so create a new one
                    recipe_item_db = RecipeItem(recipe_id=recipe_id, category_id=category_id, amount_ml=amount_ml)
                    recipe.recipe_items.append(recipe_item_db)
                else:
                    # recipe items exists, update recipe item attribute
                    recipe_item_db.amount_ml = amount_ml

            # save changes
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                return False, f"Error updating recipe: {e}"

        return True, "Recipe updated successfully"

    def update_glass(self, input_data, client_id):
        # extract input data
        glass_id = input_data.get("glassID")
        glass_data = input_data.get("value", {})

        amount_ml = glass_data.get("amount_ml")
        weight_g = glass_data.get("weight_g")

        with Session(self.engine) as session:
            # check if glass exists
            glass = session.get(Glass, glass_id)
            if glass is None:
                return False, "Glass does not exist"

            # update glass attributes
            if amount_ml is not None:
                glass.amount_ml = amount_ml
            if weight_g is not None:
                glass.weight_g = weight_g

            # save changes
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                return False, f"Error updating glass: {e}"

        return True, "Glass updated successfully"