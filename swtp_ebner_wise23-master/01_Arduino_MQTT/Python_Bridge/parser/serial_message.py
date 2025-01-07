""" SWTP_Ebner_WiSe23_Getraenkemaschine
Classes for converting serial messages to JSON

Version 0.1
Licence: MIT
"""

import json
import abc

class SerialMessage(abc.ABC):
    def __init__(self, input):
        # strip trailing whitespace
        input = input.rstrip()

        # split message into arguments
        self.arguments = input.split(",")

    @abc.abstractmethod
    def is_valid(self):
        # check if the message format is valid
        pass

    @abc.abstractmethod
    def to_json(self, sale):
        # convert the serial input to a JSON message
        pass

    @classmethod
    def create(cls, input):
        # choose implementation depending on the message type
        if input.startswith("info,"):
            return InfoMessage(input)
        elif input.startswith("error,"):
            return ErrorMessage(input)

        return UnknownMessage(input)

class InfoMessage(SerialMessage):
    def __init__(self, input):
        super().__init__(input)

    def is_valid(self):
        # check if the number of arguments is correct
        if len(self.arguments) != 2:
            return False

        # info code must be a number
        if not self.arguments[1].isdigit():
            return False

        return True

    def to_json(self):
        # build JSON as dictionary
        message_dict = {
            "type": self.arguments[0],
            "value": int(self.arguments[1]) # single info code
        }

        # convert dictionary into JSON
        json_message = json.dumps(message_dict)
        return json_message

class ErrorMessage(SerialMessage):
    def __init__(self, input):
        super().__init__(input)

    def is_valid(self):
        # check if the number of arguments is correct
        if len(self.arguments) != 3:
            return False

        # error code and error info must be numbers
        if not self.arguments[1].isdigit() or not self.arguments[2].isdigit():
            return False

        return True

    def to_json(self):
        # value consists of the error code and the error info, so create a nested dictionary
        value_dict = {
            "error_code": int(self.arguments[1]),
            "error_info": int(self.arguments[2])
        }

        # build JSON as dictionary
        message_dict = {
            "type": self.arguments[0],
            "value": value_dict
        }

        # convert dictionary into JSON
        json_message = json.dumps(message_dict)
        return json_message

class UnknownMessage(SerialMessage):
    def __init__(self, input):
        super().__init__(input)

    def is_valid(self):
        # unknown message type, cannot validate
        return False

    def to_json(self):
        # unknown message type, cannot convert
        return ""