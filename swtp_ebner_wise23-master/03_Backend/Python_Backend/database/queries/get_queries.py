""" SWTP_Ebner_WiSe23_Getraenkemaschine
Handler for get queries

Version 0.1
Licence: MIT
"""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database.model import (
    Category, Bottle, BottleItem, Machine, Recipe, RecipeItem, Glass
)

class GetHandler:
    def __init__(self, engine, util_handler):
        self.engine = engine
        self.util_handler = util_handler

    def get_bottle(self, input, client_id):
        with Session(self.engine) as session:
            # get a list of all bottles
            sql_query = select(Bottle)

            if "machineID" in input:
                # only include bottles that are loaded into at least one of the specified machines
                # (use 'distinct' to prevent duplicate bottles)
                sql_query = sql_query.join(BottleItem).distinct().where(BottleItem.machine_id.in_(input["machineID"]))

            if "bottleID" in input:
                # only include bottles that have one of the specified IDs
                sql_query = sql_query.where(Bottle.id.in_(input["bottleID"]))

            if "categoryID" in input:
                # only include bottles that belong to one of the specified categories
                sql_query = sql_query.where(Bottle.category_id.in_(input["categoryID"]))

            if "includeAlc" in input:
                # default behavior: include bottles with alcohol
                if not input["includeAlc"]:
                    # only include bottles that do not contain alcohol
                    sql_query = sql_query.where(Bottle.alcohol_percentage == 0)

            # convert to JSON
            bottle_list = [bottle.to_json() for bottle in session.scalars(sql_query)]

        # return the list of bottles as the response
        return True, bottle_list

    def get_machine(self, input, client_id):
        with Session(self.engine) as session:
            # calculate max glass volume (not machine-specific)
            glass_query = select(func.max(Glass.amount_ml))
            max_glass = session.execute(glass_query).scalar_one()

            # get a list of all machines
            machine_query = select(Machine)

            if "machineID" in input:
                # only include machines that have one of the specified IDs
                machine_query = machine_query.where(Machine.id.in_(input["machineID"]))

            # convert to JSON
            machine_list = [machine.to_json(max_glass) for machine in session.scalars(machine_query)]

        # return the list of machines as the response
        return True, machine_list

    def get_category(self, input, client_id):
        with Session(self.engine) as session:
            # get a list of all categories
            sql_query = select(Category)

            if "parent_categoryID" in input:
                # only include categories with the specified parent
                sql_query = sql_query.filter_by(parent_id=input["parent_categoryID"])

            # convert to JSON
            category_list = [category.to_json() for category in session.scalars(sql_query)]

        # return the list of categories as the response
        return True, category_list

    def get_recipe(self, input, client_id):
        with Session(self.engine) as session:
            # get a list of all recipes
            recipe_query = select(Recipe)

            if "categoryID" in input:
                # check if the recipe has one of the required categories (or a sub-category)
                recipe_query = recipe_query.where(Recipe.category_id.in_(self.util_handler.get_with_child_ids(input["categoryID"])))

            recipe_list = []
            for recipe in session.scalars(recipe_query):
                recipe_matches_filters = True

                if "contains_categoryID" in input:
                    # check if every required category (or a sub-category) is contained in the recipe
                    for category_id in input["contains_categoryID"]:
                        category_query = select(RecipeItem).filter_by(recipe_id=recipe.id)
                        category_query = category_query.where(RecipeItem.category_id.in_(self.util_handler.get_with_child_ids([category_id])))
                        first_match = session.scalars(category_query).first()

                        if first_match is None:
                            # no matching recipe item, no need to check the other categories
                            recipe_matches_filters = False
                            break

                if "includeAlc" in input or "producable_by_machineID" in input:
                    # check if there is a bottle that can be used for each recipe item according to the filter criteria
                    include_alc = input.get("includeAlc", True)
                    machine_id = input.get("producable_by_machineID", None)

                    for item in recipe.recipe_items:
                        if self.util_handler.get_matching_bottle(item.category_id, item.amount_ml, include_alc, machine_id) is None:
                            # no matching bottle, no need to check the other recipe items
                            recipe_matches_filters = False
                            break

                if recipe_matches_filters:
                    # all filter conditions are met, so add the recipe to the response
                    recipe_list.append(recipe.to_json())

        # return the list of recipes as the response
        return True, recipe_list

    def get_glass(self, input, client_id):
        with Session(self.engine) as session:
            # get a list of all glasses
            sql_query = select(Glass)

            # convert to JSON
            glass_list = [glass.to_json() for glass in session.scalars(sql_query)]

        # return the list of glasses as the response
        return True, glass_list
