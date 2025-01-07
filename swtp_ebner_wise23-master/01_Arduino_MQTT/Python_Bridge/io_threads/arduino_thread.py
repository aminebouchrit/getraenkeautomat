""" SWTP_Ebner_WiSe23_Getraenkemaschine
Communication from Arduino to backend

Version 0.1
Licence: MIT
"""

import threading

from parser.serial_message import SerialMessage

class ArduinoDataThread(threading.Thread):
    def __init__(self, mqtt_client, serial_client, send_topic):
        threading.Thread.__init__(self)
        self.mqtt_client = mqtt_client
        self.serial_client = serial_client
        self.send_topic = send_topic

    def send_to_backend(self, json_message):
        # send JSON message
        print(f"Sending message to backend: {json_message}")
        self.mqtt_client.publish(self.send_topic, json_message)

    def run(self):
        while True:
            # wait for a serial message from Arduino
            input = self.serial_client.readline().decode()

            serial_message = SerialMessage.create(input)

            # check if message format is valid
            if serial_message.is_valid():
                print("\nValid serial message received")

                # convert to JSON and send message to backend
                self.send_to_backend(serial_message.to_json())
            else:
                print(f"\nInvalid serial message discarded: {input}")
