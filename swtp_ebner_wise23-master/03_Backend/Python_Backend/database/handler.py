""" SWTP_Ebner_WiSe23_Getraenkemaschine
Database handler

Version 0.1
Licence: MIT
"""

import sqlalchemy

from database.queries.util_queries import UtilHandler
from database.queries.get_queries import GetHandler
from database.queries.order_queries import OrderHandler
from database.queries.create_queries import CreateHandler
from database.queries.delete_queries import DeleteHandler
from database.queries.update_queries import UpdateHandler

DB_USER = "root"
DB_PASSWD = "geheim"
DB_HOST = "db"
DB_PORT = 3306
DB_NAME = "drink_machine"

class Database:
    def __init__(self, frontend_publisher, machine_publisher):
        # init MariaDB connection
        url = sqlalchemy.URL.create(
            "mariadb+mariadbconnector",
            username=DB_USER,
            password=DB_PASSWD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        engine = sqlalchemy.create_engine(url)

        # setup query handlers
        self.util_handler = UtilHandler(engine)
        self.get_handler = GetHandler(engine, self.util_handler)
        self.order_handler = OrderHandler(engine, self.util_handler, frontend_publisher, machine_publisher)
        self.create_handler = CreateHandler(engine)
        self.delete_handler = DeleteHandler(engine)
        self.update_handler = UpdateHandler(engine)

        # uncomment to create the database schema from the ORM
        # database.model.Base.metadata.create_all(engine)


    # ---- handler for input from client ----

    # feed forward a request to the right handler module
    def request(self, keyWord: str, entity: str, input: dict, client_id: int):
        # choose function from the correct handler
        try:
            if entity == "order" or entity == "customorder":
                function = getattr(self.order_handler, f"{keyWord}_{entity}")
            elif keyWord == "check":
                function = getattr(self.util_handler, f"check_{entity}")
            else:
                handler = getattr(self, f"{keyWord}_handler")
                function = getattr(handler, f"{keyWord}_{entity}")
        except Exception as e:
            print(f"{e}, message discarded")
            return False, f"{keyWord}/{entity} not supported"

        # run function
        try:
            response = function(input, client_id)
        except Exception as e:
            print(f"error in {keyWord}_{entity}(): {e}, message discarded")
            return False, f"internal error with request {keyWord}/{entity}"

        return response


    # ---- handler for input from machine ----

    def on_machine_info(self, machine_id, input_data):
        self.order_handler.on_machine_info(machine_id, input_data)

    def on_machine_error(self, machine_id, input_data):
        self.order_handler.on_machine_error(machine_id, input_data)


