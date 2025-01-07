""" SWTP_Ebner_WiSe23_Getraenkemaschine
Machine JSON schema definitions

Version 0.1
Licence: MIT
"""

import enum

class SCHEMA(enum.Enum):
    info = {
        "type": "object",
        "properties": {
            "value": {
                "type": "integer",
                "minimum": 0
            }
        },
        "required": [ "value" ]
    }

    error = {
        "type": "object",
        "properties": {
            "value": {
                "type": "object",
                "properties": {
                    "error_code": {
                        "type": "integer",
                        "minimum": 0
                    },
                    "error_info": {
                        "type": "integer",
                        "minimum": 0
                    }
                },
                "required": [ "error_code", "error_info" ]
            }
        },
        "required": [ "value" ]
    }
