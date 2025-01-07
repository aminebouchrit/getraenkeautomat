""" SWTP_Ebner_WiSe23_Getraenkemaschine
Frontend listener class definition

Version 0.1
Licence: MIT
"""

import json

from database.handler import Database
from parser.json_validator import Validator
from parser.frontend_schema import SCHEMA

class FrontendListener:
    def __init__(self, mqtt_client, base_topic, publisher, db: Database):
        self.mqtt_client = mqtt_client
        self.base_topic = base_topic
        self.listen_topic = f"{base_topic}client/+/+/#"

        self.publisher = publisher
        self.db = db

        self.subscribe()

    def subscribe(self):
        def on_message(mqtt_client, userdata, msg):
            print(f"\nmessage in topic: '{msg.topic}':")

            # check if we need to listen to this topic
            # and get client_id, keyWord and entity of request
            (client_id, keyWord, entity) = self.msg_in_command_topic(msg.topic)
            if client_id is None or keyWord is None or entity is None:
                print("invalid topic, message discarded")
                return

            # check if message is retained, if so discard it because we only allow recent messages
            if msg.retain is not None and msg.retain:
                print("received retained flag, message discarded")
                return

            # to lower case to increase compatibility
            keyWord = keyWord.lower()
            entity = entity.lower()

            # check if message is valid json
            if not self.is_valid_json(msg.payload.decode()):
                print("json not valid, message discarded")
                # send response to client via its own topic
                self.publisher.send_error_to_client(client_id, "message contains invalid json")
                return

            # get data from msg
            data = json.loads(msg.payload.decode())
            print(data)

            # if this is a restricted command check for right password
            if keyWord == "update" or keyWord == "delete" or \
                (keyWord == "create" and entity != "order" and entity != "customorder" and entity != "rating"):
                success, response = self.process_command(client_id, data, "check", "credentials")
                if not success:
                    self.publisher.send_error_to_client(client_id, response)
                    return

            # send data to database handler and get required response back
            success, response = self.process_command(client_id, data, keyWord, entity)
            if success is None or not success:
                # we recieved an error from database handler
                # send response to client via its own topic
                if response is not None:
                    self.publisher.send_error_to_client(client_id, response)
                else:
                    self.publisher.send_error_to_client(client_id, "internal server error")
                return

            # we have a proper response
            # send response to client via its own topic
            self.publisher.send_to_client(client_id, entity, response)

        self.mqtt_client.message_callback_add(self.listen_topic, on_message)
        self.mqtt_client.subscribe(self.listen_topic)

    def msg_in_command_topic(self, topic: str) -> tuple[str, str, str]:
        # /THM/drinkMachine/client/<id>/<keyWord>/<Entity>
        topic = topic.removeprefix(self.base_topic)
        # client/<id>/<keyWord>/<Entity>
        #    0     1      2         3
        topic_list = topic.split("/")

        try:
            # check if the msg is published as a valid client request
            if topic_list[0] != "client" or not topic_list[1].isdigit():
                return None, None, None

            client_id = topic_list[1]
            keyWord = topic_list[2]
            entity = topic_list[3]

            # check that there is no other subtopic
            if len(topic_list) > 4:
                return None, None, None
        except IndexError:
            return None, None, None

        return client_id, keyWord, entity

    def is_valid_json(self, input):
        try:
            json.loads(input)
        except:
            return False
        return True

    def process_command(self, client_id, json_data, keyWord: str, entity: str):
        # try to find json schema definition for this request
        try:
            schema = getattr(SCHEMA, f"{keyWord}_{entity}")
            schema_defined = True
        except Exception as e:
            schema_defined = False
            print(f"info: json-schema for {e} not defined")

        # check if request contains json in correct format and with correct types
        error_msg = False
        if schema_defined:
            error_msg = Validator.validate(json_data, schema.value)
        if error_msg:
            print(f"{error_msg}, message discarded")
            return False, error_msg

        # run neccessary method for this request
        # and return data that the client requested
        return self.db.request(keyWord, entity, json_data, client_id)
