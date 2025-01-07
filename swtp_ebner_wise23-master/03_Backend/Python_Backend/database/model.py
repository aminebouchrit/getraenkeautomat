""" SWTP_Ebner_WiSe23_Getraenkemaschine
Database definition

Version 0.1
Licence: MIT
"""

import enum

from sqlalchemy import (
    Column, ForeignKey, Integer, Numeric,
    Text, String, DateTime, Enum
)
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    # base class that is responsible for mapping classes to tables
    pass

class User(Base):
    __tablename__ = "user"

    # regular attributes
    id = Column("userID", Integer, nullable=False, primary_key=True)
    name = Column(Text, nullable=False)
    password = Column(String(20), nullable=False)

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, password={self.password!r})"

class Category(Base):
    __tablename__ = "category"

    # regular attributes
    id = Column("categoryID", Integer, nullable=False, primary_key=True)
    name = Column(Text, nullable=False)

    # foreign keys
    parent_id = Column("parent_categoryID", Integer, ForeignKey("category.categoryID"), nullable=True)

    # relationships
    children = relationship("Category") # categories that have this category as the parent category

    def with_children(self):
        category_list = [self.id]

        # recursively add the ids of all child categories
        for child in self.children:
            category_list.extend(child.with_children())

        return category_list

    def to_json(self):
        json_format = {
            "categoryID": self.id,
            "parent_categoryID": self.parent_id,
            "name": self.name
        }
        return json_format

    def __repr__(self):
        return f"Category(id={self.id!r}, parent_id={self.parent_id!r}, name={self.name!r})"

class Bottle(Base):
    __tablename__ = "bottle"

    # regular attributes
    id = Column("bottleID", Integer, nullable=False, primary_key=True)
    name = Column(Text, nullable=False)
    density = Column(Numeric(10, 3), nullable=False)
    max_capacity = Column(Integer, nullable=False)
    alcohol_percentage = Column(Numeric(5, 2), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    pic_url = Column(Text, nullable=False)

    # foreign keys
    category_id = Column("categoryID", Integer, ForeignKey("category.categoryID"), nullable=False)

    def to_json(self):
        json_format = {
            "bottleID": self.id,
            "categoryID": self.category_id,
            "name": self.name,
            "density": float(self.density),
            "max_capacity": self.max_capacity,
            "alcohol_percentage": float(self.alcohol_percentage),
            "price": float(self.price),
            "pic_url": self.pic_url
        }
        return json_format

    def __repr__(self):
        return f"Bottle(id={self.id!r}, name={self.name!r}, density={self.density!r}, max_capacity={self.max_capacity!r},\
            alcohol_percentage={self.alcohol_percentage!r}, price={self.price!r}, pic_url={self.pic_url!r})"

class Machine(Base):
    __tablename__ = "machine"

    # regular attributes
    id = Column("machineID", Integer, nullable=False, primary_key=True)
    name = Column(Text, nullable=False)

    # relationships
    bottle_items = relationship("BottleItem", cascade="all, delete-orphan") # bottle items that belong to this machine

    def to_json(self, max_glass):
        json_format = {
            "machineID": self.id,
            "name": self.name,
            "maxGlass": max_glass,
            "contains": [item.to_json() for item in self.bottle_items]
        }
        return json_format

    def __repr__(self):
        return f"Machine(id={self.id!r}, name={self.name!r})"

class BottleItem(Base):
    __tablename__ = "bottleitem"

    # regular attributes
    id = Column("bottleItemID", Integer, nullable=False, primary_key=True)
    position_cm = Column(Integer, nullable=False)
    pump_pin = Column(Integer, nullable=False)
    led_pin = Column(Integer, nullable=False)
    current_capacity = Column(Integer, nullable=False)

    # foreign keys
    machine_id = Column("machineID", Integer, ForeignKey("machine.machineID", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    bottle_id = Column("bottleID", Integer, ForeignKey("bottle.bottleID"), nullable=False)

    def to_json(self):
        json_format = {
            "bottleID": self.bottle_id,
            "position_cm": self.position_cm,
            "pump_pin": self.pump_pin,
            "led_pin": self.led_pin,
            "current_capacity": self.current_capacity
        }
        return json_format

    def __repr__(self):
        return f"BottleItem(id={self.id!r}, position_cm={self.position_cm!r}, pump_pin={self.pump_pin!r},\
                led_pin={self.led_pin}, current_capacity={self.current_capacity}, machine_id={self.machine_id!r},\
                bottle_id={self.bottle_id!r})"

class Glass(Base):
    __tablename__ = "glass"

    # regular attributes
    id = Column("glassID", Integer, nullable=False, primary_key=True)
    amount_ml = Column(Integer, nullable=False)
    weight_g = Column(Integer, nullable=False)

    def to_json(self):
        json_format = {
            "glassID": self.id,
            "amount_ml": self.amount_ml,
            "weight_g": self.weight_g
        }
        return json_format

    def __repr__(self):
        return f"Glass(id={self.id!r}, amount_ml={self.amount_ml!r}, weight_g={self.weight_g!r})"

class Recipe(Base):
    __tablename__ = "recipe"

    # regular attributes
    id = Column("recipeID", Integer, nullable=False, primary_key=True)
    name = Column(Text, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    pic_url = Column(Text, nullable=False)
    rating_value = Column(Numeric(3, 2), nullable=False, default=0.0)
    rating_number = Column(Integer, nullable=False, default=0)

    # foreign keys
    category_id = Column("categoryID", Integer, ForeignKey("category.categoryID"), nullable=False)
    glass_id = Column("glassID", Integer, ForeignKey("glass.glassID"), nullable=False)

    # relationships
    recipe_items = relationship("RecipeItem", order_by="RecipeItem.id", cascade="all, delete-orphan") # recipe items that are part of this recipe

    def to_json(self):
        # append list of recipe items to data
        json_format = {
            "recipeID": self.id,
            "categoryID": self.category_id,
            "name": self.name,
            "price": float(self.price),
            "pic_url": self.pic_url,
            "rating_value": float(self.rating_value),
            "rating_number": self.rating_number,
            "items": [item.to_json() for item in self.recipe_items]
        }
        return json_format

    def __repr__(self):
        return f"Recipe(id={self.id!r}, name={self.name!r}, price={self.price!r}, pic_url={self.pic_url!r}, rating_value={self.rating_value!r}, rating_number={self.rating_number!r})"

class RecipeItem(Base):
    __tablename__ = "recipeitem"

    # regular attributes
    id = Column("recipeItemID", Integer, nullable=False, primary_key=True)
    amount_ml = Column(Integer, nullable=False)

    # foreign keys
    recipe_id = Column("recipeID", Integer, ForeignKey("recipe.recipeID", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    category_id = Column("categoryID", Integer, ForeignKey("category.categoryID"), nullable=False)

    def to_json(self):
        json_format = {
            "categoryID": self.category_id,
            "amount_ml": self.amount_ml
        }
        return json_format

    def __repr__(self):
        return f"RecipeItem(id={self.id!r}, amount_ml={self.amount_ml!r}, recipe_id={self.recipe_id!r}, category_id={self.category_id!r})"

class OrderStatus(enum.Enum):
    completed = 0
    pending = 1 # order is being processed by the machine
    waiting = 2 # order was received, but has not been sent to the machine yet
    failed = 3 # order could not be completed properly

class Order(Base):
    __tablename__ = "order"

    # regular attributes
    id = Column("orderID", Integer, nullable=False, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    last_update = Column(DateTime, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False)
    client_id = Column("clientID", Integer, nullable=False)

    # foreign keys
    recipe_id = Column("recipeID", Integer, ForeignKey("recipe.recipeID", ondelete="SET NULL", onupdate="SET NULL"), nullable=True)
    glass_id = Column("glassID", Integer, ForeignKey("glass.glassID"), nullable=False)
    machine_id = Column("machineID", Integer, ForeignKey("machine.machineID", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    # relationships
    order_items = relationship("OrderItem", order_by="OrderItem.id", cascade="all, delete-orphan") # order items that are part of this recipe
    glass = relationship("Glass") # glass that the order is filled in

    def __repr__(self):
        return f"Order(id={self.id!r}, start_time={self.time!r}, last_update={self.last_update!r}, status={self.status!r},\
            client_id={self.client_id!r}, recipe_id={self.recipe_id!r}, glass_id={self.glass_id!r}, machine_id={self.machine_id!r})"

class OrderItem(Base):
    __tablename__ = "orderitem"

    # regular attributes
    id = Column("orderItemID", Integer, nullable=False, primary_key=True)
    amount_ml = Column(Integer, nullable=False)

    # foreign keys
    order_id = Column("orderID", Integer, ForeignKey("order.orderID", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    bottle_id = Column("bottleID", Integer, ForeignKey("bottle.bottleID"), nullable=False)

    def __repr__(self):
        return f"OrderItem(id={self.id!r}, amount_ml={self.amount_ml!r},order_id={self.order_id!r}, bottle_id={self.bottle_id!r})"