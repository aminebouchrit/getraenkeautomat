""" SWTP_Ebner_WiSe23_Getraenkemaschine
Machine publisher class definition

Version 0.1
Licence: MIT
"""

import json

class MachinePublisher:
    def __init__(self, mqtt_client, base_topic):
        self.mqtt_client = mqtt_client
        self.base_topic = base_topic

    def send_to_bridge(self, machine_id: int, json_msg):
        # convert dictionary into JSON
        # (use ensure_ascii to preserve unicode characters)
        payload = json.dumps(json_msg, ensure_ascii=False)

        # publish in machine-specific topic
        send_topic = f"{self.base_topic}machine/{machine_id}/fromBackend"
        self.mqtt_client.publish(send_topic, payload)
        print(f"message sent to machine {machine_id}")