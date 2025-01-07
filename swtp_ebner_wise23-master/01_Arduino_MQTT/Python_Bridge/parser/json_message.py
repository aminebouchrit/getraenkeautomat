""" SWTP_Ebner_WiSe23_Getraenkemaschine
Classes for converting JSON to serial messages

Version 0.1
Licence: MIT
"""

import json
import jsonschema
import abc

class JSONMessage(abc.ABC):
    def __init__(self, data):
        self.data = data

    def is_valid(self):
        # check if the message format is valid
        # by validating it using a JSON schema
        try:
            jsonschema.validate(self.data, self.get_schema())
        except jsonschema.exceptions.ValidationError:
            return False

        return True

    @abc.abstractmethod
    def get_schema(self):
        # return JSON that the message should be validated with
        pass

    @abc.abstractmethod
    def to_serial(self):
        # convert the JSON input to a list of serial messages
        pass

    @classmethod
    def is_valid_json(cls, input):
        # check if the input can be parsed as a JSON message
        try:
            json.loads(input)
            return True
        except ValueError:
            return False

    @classmethod
    def create(cls, input):
        if cls.is_valid_json(input):
            data = json.loads(input)

            # check if a message type was given
            if isinstance(data, dict) and "type" in data:
                # choose implementation depending on the message type
                if data["type"] == "config":
                    return ConfigMessage(data)
                elif data["type"] == "order":
                    return OrderMessage(data)
                elif data["type"] == "led":
                    return LEDMessage(data)

        return UnknownMessage(input)

class ConfigMessage(JSONMessage):
    SCHEMA = {
        "type": "object",
        "properties": {
            "value": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "configID": {
                            "type": "integer",
                            "minimum": 0
                        },
                        "stationID": {
                            "type": "integer",
                            "minimum": 0
                        },
                        "position": {
                            "type": "integer",
                            "minimum": 0
                        }
                    },
                    "required": [ "configID", "stationID", "position" ]
                },
                "minItems": 1
            }
        },
        "required": [ "value" ]
    }

    def __init__(self, data):
        super().__init__(data)

    def get_schema(self):
        return self.SCHEMA

    def station_to_serial(self, station):
        # append all values inside the station dictionary to the message
        # the values cannot be accessed by name because they depend on the station type
        serial_message = "config"
        for pos in station:
            pos_value = station[pos]
            serial_message += f",{pos_value}"
        return serial_message

    def to_serial(self):
        # each station definition is converted into its own line
        message_list = [self.station_to_serial(station) for station in self.data["value"]]

        return message_list

class OrderMessage(JSONMessage):
    SCHEMA = {
        "type": "object",
        "properties": {
            "glass_weight": {
                "type": "integer",
                "exclusiveMinimum": 0
            },
            "value": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "stationID": {
                            "type": "integer",
                            "minimum": 0
                        },
                        "value": {
                            "type": "integer",
                            "minimum": 0
                        }
                    },
                    "required": [ "stationID", "value" ]
                },
                "minItems": 1
            }
        },
        "required": [ "glass_weight", "value" ]
    }

    def __init__(self, data):
        super().__init__(data)

    def get_schema(self):
        return self.SCHEMA

    def entry_to_serial(self, order_entry):
        # each order entry order consists of two values
        id = order_entry["stationID"]
        value = order_entry["value"]
        serial_message = f",{id},{value}"
        return serial_message

    def to_serial(self):
        # construct config part of the message
        num_stations = len(self.data["value"])
        glass_weight = self.data["glass_weight"]
        serial_message = f"order,{num_stations},{glass_weight}"

        # add each included order entry to the message
        for order_entry in self.data["value"]:
            serial_message += self.entry_to_serial(order_entry)

        # store message in a list so that all 'to_serial' functions have a consistent return value
        message_list = [serial_message]
        return message_list

class LEDMessage(JSONMessage):
    SCHEMA = {
        "type": "object",
        "properties": {
            "value": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "stationID": {
                            "type": "integer",
                            "minimum": 0
                        },
                        "colorID": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 2
                        }
                    },
                    "required": [ "stationID", "colorID" ]
                },
                "minItems": 1
            }
        },
        "required": [ "value" ]
    }

    def __init__(self, data):
        super().__init__(data)

    def get_schema(self):
        return self.SCHEMA

    def config_to_serial(self, config):
        # append station ID and LED color to the message
        id = config["stationID"]
        color = config["colorID"]
        serial_message = f"led,{id},{color}"
        return serial_message

    def to_serial(self):
        # each station definition is converted into its own line
        message_list = [self.config_to_serial(config) for config in self.data["value"]]

        return message_list

class UnknownMessage(JSONMessage):
    SCHEMA = {}

    def __init__(self, data):
        super().__init__(data)

    def is_valid(self):
        # unknown message type, cannot validate
        return False

    def get_schema(self):
        # there is no useful schema for an unknown message type
        return self.SCHEMA

    def to_serial(self):
        # unknown message type, cannot convert
        return []