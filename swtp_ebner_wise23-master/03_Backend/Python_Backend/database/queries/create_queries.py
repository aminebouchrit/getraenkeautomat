""" SWTP_Ebner_WiSe23_Getraenkemaschine
Handler for create queries (except for order creation)

Version 0.1
Licence: MIT
"""

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database.model import (
    Category, Bottle, BottleItem, Machine, Recipe, RecipeItem, Glass
)

class CreateHandler:
    def __init__(self, engine):
        self.engine = engine

    def create_bottle(self, input_data, client_id):
        # extract input data
        bottle_data = input_data.get("value", {})

        category_id = bottle_data.get("categoryID")
        name = bottle_data.get("name")
        density = bottle_data.get("density")
        max_capacity = bottle_data.get("max_capacity")
        alcohol_percentage = bottle_data.get("alcohol_percentage")
        price = bottle_data.get("price")
        pic_url = bottle_data.get("pic_url")

        with Session(self.engine) as session:
            # check if category exists
            existing_category = session.get(Category, category_id)
            if existing_category is None:
                return False, "Category does not exist"

            # check if a bottle with the same name already exists
            existing_bottle = session.execute(select(Bottle).filter_by(name=name)).first()
            if existing_bottle is not None:
                return False, "Bottle already exists"

            # create new bottle object
            new_bottle = Bottle(
                category_id=category_id,
                name=name,
                density=density,
                max_capacity=max_capacity,
                alcohol_percentage=alcohol_percentage,
                price=price,
                pic_url=pic_url
            )

            # add new bottle to the database
            try:
                session.add(new_bottle)
                session.commit()
            except IntegrityError as e:
                session.rollback()
                return False, f"Error creating bottle: {e}"

        # return success response
        return True, "Bottle created successfully"

    def create_machine(self, input_data, client_id):
        # extract input data
        machine_data = input_data.get("value", {})

        machine_name = machine_data.get("name")
        bottle_item_data = machine_data.get("bottle_items", [])

        with Session(self.engine) as session:
            # check if a machine with the same name already exists
            existing_machine = session.execute(select(Machine).filter_by(name=machine_name)).first()
            if existing_machine is not None:
                return False, "Machine already exists"

            # create new machine object
            new_machine = Machine(name=machine_name)

            # create new bottle items and add them to the machine
            for bottle_item in bottle_item_data:
                position_cm = bottle_item.get("position_cm")
                pump_pin = bottle_item.get("pump_pin")
                led_pin = bottle_item.get("led_pin")
                current_capacity = bottle_item.get("current_capacity")
                bottle_id = bottle_item.get("bottleID")

                # check if the referenced bottle exists
                bottle = session.get(Bottle, bottle_id)
                if bottle is None:
                    return False, f"Bottle with id {bottle_id} does not exist"

                new_bottle_item = BottleItem(position_cm=position_cm, pump_pin=pump_pin, led_pin=led_pin,
                                             current_capacity=current_capacity, bottle_id=bottle_id)
                new_machine.bottle_items.append(new_bottle_item)

            # add new machine to the database
            try:
                session.add(new_machine)
                session.commit()
            except IntegrityError as e:
                session.rollback()
                return False, f"Error creating machine: {e}"

        # return success response
        return True, "Machine created successfully"

    def create_category(self, input_data, client_id):
        # extract input data
        category_data = input_data.get("value", {})

        parent_id = category_data.get("parent_categoryID")
        name = category_data.get("name")

        with Session(self.engine) as session:
            # check if parent category exists (if this is a sub-category)
            if parent_id is not None:
                existing_parent = session.get(Category, parent_id)
                if existing_parent is None:
                    return False, "Parent category does not exist"

            # check if a category with the same name already exists
            existing_category = session.execute(select(Category).filter_by(name=name)).first()
            if existing_category is not None:
                return False, "Category already exists"

            # create new category object
            new_category = Category(
                parent_id=parent_id,
                name=name
            )

            # add new category to the database
            try:
                session.add(new_category)
                session.commit()
            except IntegrityError as e:
                session.rollback()
                return False, f"Error creating category: {e}"

        # return success response
        return True, "Category created successfully"

    def create_recipe(self, input_data, client_id):
        # extract input data
        recipe_data = input_data.get("value", {})

        recipe_name = recipe_data.get("name")
        recipe_price = recipe_data.get("price")
        recipe_pic_url = recipe_data.get("pic_url")
        recipe_category_id = recipe_data.get("categoryID")
        recipe_glass_id = recipe_data.get("glassID")
        recipe_items_data = recipe_data.get("recipe_items", [])

        with Session(self.engine) as session:
            # check if category exists
            existing_category = session.get(Category, recipe_category_id)
            if existing_category is None:
                return False, "Category does not exist"

            # check if glass exists
            existing_glass = session.get(Glass, recipe_glass_id)
            if existing_glass is None:
                return False, "Glass does not exist"

            # check if a recipe with the same name already exists
            existing_recipe = session.execute(select(Recipe).filter_by(name=recipe_name)).first()
            if existing_recipe is not None:
                return False, "Recipe already exists"

            # create a new recipe object
            recipe = Recipe(
                name=recipe_name,
                price=recipe_price,
                pic_url=recipe_pic_url,
                category_id=recipe_category_id,
                glass_id=recipe_glass_id
            )

            # create new recipe items and add them to the recipe
            for recipe_item_data in recipe_items_data:
                category_id = recipe_item_data.get("categoryID")
                amount_ml = recipe_item_data.get("amount_ml")

                # check if category exists
                existing_category = session.get(Category, category_id)
                if existing_category is None:
                    return False, f"Category with id {category_id} does not exist"

                recipe_item = RecipeItem(category_id=category_id, amount_ml=amount_ml)
                recipe.recipe_items.append(recipe_item)

            # add new recipe to the database
            try:
                session.add(recipe)
                session.commit()
            except IntegrityError as e:
                session.rollback()
                return False, f"Error creating recipe: {e}"

        # return success response
        return True, "Recipe created successfully"

    def create_rating(self, input_data, client_id):
        # extract input data
        recipe_id = input_data["recipeID"]
        rating_value = input_data["rating_value"]

        with Session(self.engine) as session:
            # check if recipe exists
            recipe = session.get(Recipe, recipe_id)
            if recipe is None:
                return False, "Recipe does not exist"

            # calculate new rating
            # the number of ratings is used so that new ratings are weighted correctly
            new_rating_number = recipe.rating_number + 1
            new_rating_value = (float(recipe.rating_value) * recipe.rating_number + rating_value) / new_rating_number

            # save changes
            recipe.rating_value = new_rating_value
            recipe.rating_number = new_rating_number

            session.commit()

        return True, "Rating received"

    def create_glass(self, input_data, client_id):
        # extract input data
        glass_data = input_data.get("value", {})

        amount_ml = glass_data.get("amount_ml")
        weight_g = glass_data.get("weight_g")

        with Session(self.engine) as session:
            # create new glass object
            new_glass = Glass(
                amount_ml=amount_ml,
                weight_g=weight_g
            )

            # add new glass to the database
            try:
                session.add(new_glass)
                session.commit()
            except IntegrityError as e:
                session.rollback()
                return False, f"Error creating glass: {e}"

        # return success response
        return True, "Glass created successfully"