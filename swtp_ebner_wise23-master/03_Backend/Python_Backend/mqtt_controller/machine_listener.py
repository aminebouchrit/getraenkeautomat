""" SWTP_Ebner_WiSe23_Getraenkemaschine
Machine listener class definition

Version 0.1
Licence: MIT
"""

import json

from database.handler import Database
from parser.json_validator import Validator
from parser.machine_schema import SCHEMA

class MachineListener:
    def __init__(self, mqtt_client, base_topic, db: Database):
        self.mqtt_client = mqtt_client
        self.base_topic = base_topic
        self.listen_topic = f"{base_topic}machine/+/toBackend"

        self.db = db

        self.subscribe()

    def subscribe(self):
        def on_message(mqtt_client, userdata, msg):
            self.process_message(msg.topic, msg.payload.decode())

        self.mqtt_client.message_callback_add(self.listen_topic, on_message)
        self.mqtt_client.subscribe(self.listen_topic)

    def is_valid_json(self, input):
        try:
            json.loads(input)
        except:
            return False
        return True

    def process_message(self, topic, message):
        # extract machine ID from topic
        topic_list = topic.removeprefix(self.base_topic).split("/")
        # machine/<id>/toBackend
        #    0      1       2
        machine_id = topic_list[1]
        print(f"\nmessage from machine {machine_id}:")

        # check if machine ID is a number
        if not machine_id.isdigit():
            print("machine id is invalid, message discarded")
            return

        # check if message is valid json
        if not self.is_valid_json(message):
            print("json not valid, message discarded")
            return

        json_message = json.loads(message)
        print(json_message)

        # check if the message has a valid type
        if not "type" in json_message or (json_message["type"] != "info" and json_message["type"] != "error"):
            print("type is missing or invalid, message discarded")
            return

        # check if request contains json in correct format and with correct types
        schema = SCHEMA.info if json_message["type"] == "info" else SCHEMA.error
        error_msg = Validator.validate(json_message, schema.value)
        if error_msg:
            print(f"{error_msg}, message discarded")
            return

        # call handler function depending on the message type
        if json_message["type"] == "info":
            self.db.on_machine_info(machine_id, json_message["value"])
        elif json_message["type"] == "error":
            self.db.on_machine_error(machine_id, json_message["value"])
