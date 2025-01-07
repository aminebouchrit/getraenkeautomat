""" SWTP_Ebner_WiSe23_Getraenkemaschine
Handler for delete queries

Version 0.1
Licence: MIT
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database.model import (
    Category, Bottle, Machine, Recipe, Glass
)

class DeleteHandler:
    def __init__(self, engine):
        self.engine = engine

    def delete_bottle(self, input_data, client_id):
        # extract input data
        bottle_id = input_data["bottleID"]

        with Session(self.engine) as session:
            # check if bottle exists
            bottle = session.get(Bottle, bottle_id)
            if bottle is None:
                return False, "Bottle does not exist"

            # delete bottle
            try:
                session.delete(bottle)
                session.commit()
            except IntegrityError as e:
                # can occur if a foreign key constraint fails
                session.rollback()
                return False, f"Error deleting bottle: {e}"

        return True, "Bottle deleted successfully"

    def delete_machine(self, input_data, client_id):
        # extract input data
        machine_id = input_data["machineID"]

        with Session(self.engine) as session:
            # check if machine exists
            machine = session.get(Machine, machine_id)
            if machine is None:
                return False, "Machine does not exist"

            # delete machine
            try:
                session.delete(machine)
                session.commit()
            except IntegrityError as e:
                # can occur if a foreign key constraint fails
                session.rollback()
                return False, f"Error deleting machine: {e}"

        return True, "Machine deleted successfully"

    def delete_category(self, input_data, client_id):
        # extract input data
        category_id = input_data["categoryID"]

        with Session(self.engine) as session:
            # check if category exists
            category = session.get(Category, category_id)
            if category is None:
                return False, "Category does not exist"

            # delete category
            try:
                session.delete(category)
                session.commit()
            except IntegrityError as e:
                # can occur if a foreign key constraint fails
                session.rollback()
                return False, f"Error deleting category: {e}"

        return True, "Category deleted successfully"

    def delete_recipe(self, input_data, client_id):
        # extract input data
        recipe_id = input_data["recipeID"]

        with Session(self.engine) as session:
            # check if recipe exists
            recipe = session.get(Recipe, recipe_id)
            if not recipe:
                return False, "Recipe does not exist"

            # delete recipe
            try:
                session.delete(recipe)
                session.commit()
            except IntegrityError as e:
                # can occur if a foreign key constraint fails
                session.rollback()
                return False, f"Error deleting recipe: {e}"

        return True, "Recipe deleted successfully"

    def delete_glass(self, input_data, client_id):
        # extract input data
        glass_id = input_data["glassID"]

        with Session(self.engine) as session:
            # check if glass exists
            glass = session.get(Glass, glass_id)
            if glass is None:
                return False, "Glass does not exist"

            # delete glass
            try:
                session.delete(glass)
                session.commit()
            except IntegrityError as e:
                # can occur if a foreign key constraint fails
                session.rollback()
                return False, f"Error deleting glass: {e}"

        return True, "Glass deleted successfully"