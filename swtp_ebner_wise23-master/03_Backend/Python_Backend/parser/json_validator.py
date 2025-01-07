""" SWTP_Ebner_WiSe23_Getraenkemaschine
JSON schema validation

Version 0.1
Licence: MIT
"""

import jsonschema

class Validator:
    @classmethod
    def validate(cls, input, schema):
        try:
            jsonschema.validate(input, schema)
        except jsonschema.exceptions.ValidationError as e:
            # message is invalid
            return f"incorrect message: {e.message}"
        except jsonschema.exceptions.SchemaError as e:
            # schema is invalid, so the message cannot be validated
            return f"schema error: {e.message} at {e.path}"

        # message is valid
        return None
