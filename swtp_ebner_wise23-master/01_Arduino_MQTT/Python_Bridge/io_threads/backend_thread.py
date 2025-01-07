""" SWTP_Ebner_WiSe23_Getraenkemaschine
Communication from backend to Arduino

Version 0.1
Licence: MIT
"""

import threading
import time

from parser.json_message import JSONMessage

class BackendDataThread(threading.Thread):
    def __init__(self, mqtt_client, serial_client, receive_topic):
        threading.Thread.__init__(self)
        self.mqtt_client = mqtt_client
        self.serial_client = serial_client
        self.receive_topic = receive_topic

    def send_to_arduino(self, message_list):
        # some JSON messages (e.g.: config) correspond to multiple lines in the serial format
        # in these cases, the lines are sent to the Arduino one after the other
        for line in message_list:
            print(f"Sending message to Arduino: {line}")
            self.serial_client.write(line.encode())
            time.sleep(2) # wait to prevent serial buffer overflow

    def subscribe(self):
        def on_message(client, userdata, msg):
            input = msg.payload.decode()

            json_message = JSONMessage.create(input)

            # check if message format is valid
            if json_message.is_valid():
                print("\nValid json message received")

                # convert to serial format and send message to Arduino
                self.send_to_arduino(json_message.to_serial())
            else:
                print(f"\nInvalid json message discarded: {input}")

        # subscribe to topic
        self.mqtt_client.on_message = on_message
        self.mqtt_client.subscribe(self.receive_topic)

    def run(self):
        # subscribe to topic on thread start, then wait for MQTT messages
        self.subscribe()
        self.mqtt_client.loop_forever()
