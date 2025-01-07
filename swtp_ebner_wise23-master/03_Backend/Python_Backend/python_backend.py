#!/usr/bin/env python3
""" SWTP_Ebner_WiSe23_Getraenkemaschine
Main File for the backend

Version 0.1
Licence: MIT
"""

import sys
import random
import paho.mqtt.client

from database.handler import Database
from mqtt_controller.machine_publisher import MachinePublisher
from mqtt_controller.frontend_publisher import FrontendPublisher
from mqtt_controller.machine_listener import MachineListener
from mqtt_controller.frontend_listener import FrontendListener

MQTT_BROKER = "broker.mqttdashboard.com" # broker that handles the MQTT messages
MQTT_PORT = 1883
MQTT_BASE_TOPIC = "THM/drinkMachine/"
MQTT_BACKEND_ID = f"python-mqtt-server-{random.randint(0, 3000)}" # used by the broker to identify the backend

def connect_mqtt() -> paho.mqtt.client.Client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker: '{MQTT_BROKER}:{MQTT_PORT}'")
            print(f"The client ID of this MQTT client is: '{MQTT_BACKEND_ID}'")
        else:
            print(f"Failed to connect to the MQTT broker (return code: {rc})!")
            sys.exit(rc)

    # try to connect to the MQTT broker
    mqtt_client = paho.mqtt.client.Client(MQTT_BACKEND_ID)
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
    return mqtt_client

def run():
    # create mqtt client
    mqtt_client = connect_mqtt()

    # create publishers
    frontend_publisher = FrontendPublisher(mqtt_client, MQTT_BASE_TOPIC)
    machine_publisher = MachinePublisher(mqtt_client, MQTT_BASE_TOPIC)

    # create database connection
    db = Database(frontend_publisher, machine_publisher)

    # create listener for requests from the frontend
    FrontendListener(mqtt_client, MQTT_BASE_TOPIC, frontend_publisher, db)

    # create listener for messages from the drink machines
    MachineListener(mqtt_client, MQTT_BASE_TOPIC, db)

    try:
        # wait for MQTT messages
        mqtt_client.loop_forever()
    except KeyboardInterrupt:
        print("Server stopped")

if __name__ == "__main__":
    run()
