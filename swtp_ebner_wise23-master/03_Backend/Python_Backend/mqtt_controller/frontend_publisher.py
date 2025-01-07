""" SWTP_Ebner_WiSe23_Getraenkemaschine
Frontend publisher class definition

Version 0.1
Licence: MIT
"""

import json

class FrontendPublisher:
    def __init__(self, mqtt_client, base_topic):
        self.mqtt_client = mqtt_client
        self.base_topic = base_topic

    def send_to_client(self, client_id: int, response_type: str, msg_value):
        # build json response
        response = {
            "response": response_type,
            "value": msg_value
        }

        # convert dictionary into JSON
        # (use ensure_ascii to preserve unicode characters)
        payload = json.dumps(response, ensure_ascii=False)

        # publish in client-specific topic
        send_topic = f"{self.base_topic}client/{client_id}"
        self.mqtt_client.publish(send_topic, payload)
        if type(msg_value) == str:
            # log info/error messages
            print(f"response sent to client {client_id}:\n{msg_value}")
        else:
            print(f"response sent to client {client_id}")

    def send_error_to_client(self, client_id: int, msg):
        # utility function for sending error messages
        self.send_to_client(client_id, "error", msg)