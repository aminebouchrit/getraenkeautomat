""" SWTP_Ebner_WiSe23_Getraenkemaschine
Handler for util queries that do not fit into another category

Version 0.1
Licence: MIT
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.model import (
    User, Category, Bottle, BottleItem
)

class UtilHandler:
    def __init__(self, engine):
        self.engine = engine

    # ---- external (used by the listeners)

    def check_credentials(self, input_data, client_id):
        with Session(self.engine) as session:
            # verify credentials
            sql_query = select(User).filter_by(name=input_data["name"], password=input_data["password"])

            if session.execute(sql_query).one_or_none() is not None:
                # given credentials are present in database
                return True, "Access granted"

        # given credentials are invalid
        return False, "Access denied"


    # ---- internal (used by other queries) ----

    def get_with_child_ids(self, category_ids):
        with Session(self.engine) as session:
            # get specified categories
            categories = session.scalars(select(Category).where(Category.id.in_(category_ids)))

            # expand list of categories to include sub-categories
            category_ids = []
            for category in categories:
                category_ids.extend(category.with_children())
        return category_ids

    def get_matching_bottle(self, category_id, amount_ml, include_alc, machine_id):
        with Session(self.engine) as session:
            # get a list of all bottles that belong to the specified category (or a sub-category)
            bottle_query = select(Bottle)
            bottle_query = bottle_query.where(Bottle.category_id.in_(self.get_with_child_ids([category_id])))

            if machine_id is not None:
                # only take bottles into account that are loaded into the specified machine
                # and that still have enough capacity
                bottle_query = bottle_query.join(BottleItem).where(BottleItem.machine_id == machine_id)
                bottle_query = bottle_query.where(BottleItem.current_capacity >= amount_ml)

            if not include_alc:
                # only take bottles into account that do not contain alcohol
                bottle_query = bottle_query.where(Bottle.alcohol_percentage == 0)

            # find a matching bottle
            # return 'None' if no matching bottle was found
            matching_bottle = session.scalars(bottle_query).first()

        return matching_bottle