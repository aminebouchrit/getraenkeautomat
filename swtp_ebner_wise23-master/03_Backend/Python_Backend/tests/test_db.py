""" SWTP_Ebner_WiSe23_Getraenkemaschine
Tests for database queries

Version 0.1
Licence: MIT
"""

import unittest
import sqlalchemy

from sqlalchemy.orm import Session

from database.handler import Database
from database.queries.util_queries import UtilHandler
from database.queries.get_queries import GetHandler
from database.queries.order_queries import OrderHandler
from database.queries.create_queries import CreateHandler
from database.queries.delete_queries import DeleteHandler
from database.queries.update_queries import UpdateHandler
from database.model import Base, Category

class TestFrontendPublisher:
    def send_to_client(self, client_id: int, response_type: str, msg_value):
        # empty so no messages are sent when running tests
        pass

class TestMachinePublisher:
    def send_to_bridge(self, machine_id: int, json_msg):
        # empty so no messages are sent when running tests
        pass

class TestHandler(Database):
        def __init__(self, frontend_publisher, machine_publisher):
            # setup connection to in-memory SQLite database used for testing
            # (executed before each test case)
            engine = sqlalchemy.create_engine("sqlite://")

            # use ORM to setup tables
            Base.metadata.create_all(engine)

            # setup query handlers
            self.util_handler = UtilHandler(engine)
            self.get_handler = GetHandler(engine, self.util_handler)
            self.order_handler = OrderHandler(engine, self.util_handler, frontend_publisher, machine_publisher)
            self.create_handler = CreateHandler(engine)
            self.delete_handler = DeleteHandler(engine)
            self.update_handler = UpdateHandler(engine)

            # add test data
            with Session(engine) as session:
                session.add(Category(id=1, name="Getränke", parent_id=None))
                session.add(Category(id=2, name="Softdrinks", parent_id=1))
                session.add(Category(id=3, name="Cola", parent_id=2))
                session.add(Category(id=4, name="Fanta", parent_id=2))
                session.commit()

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # setup database
        self.db = TestHandler(TestFrontendPublisher(), TestMachinePublisher())

    def test_get_category(self):
        # test query without filter
        success, response = self.db.request("get", "category", {}, 1)
        expected_response = [
            { "categoryID": 1, "parent_categoryID": None, "name": "Getränke" },
            { "categoryID": 2, "parent_categoryID": 1, "name": "Softdrinks" },
            { "categoryID": 3, "parent_categoryID": 2, "name": "Cola" },
            { "categoryID": 4, "parent_categoryID": 2, "name": "Fanta" }
        ]
        self.assertTrue(success, True)
        self.assertCountEqual(response, expected_response) # test if the list items are equal (regardless of the order)

        # test query with filter option
        success, response = self.db.request("get", "category", {"parent_categoryID": 2}, 1)
        expected_response = [
            { "categoryID": 3, "parent_categoryID": 2, "name": "Cola" },
            { "categoryID": 4, "parent_categoryID": 2, "name": "Fanta" }
        ]
        self.assertTrue(success, True)
        self.assertCountEqual(response, expected_response)

if __name__ == '__main__':
    unittest.main()