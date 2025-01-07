#!/usr/bin/env python3
""" SWTP_Ebner_WiSe23_Getraenkemaschine
Main File for the python bridge

Version 0.1
Licence: MIT
"""

import sys
import time
import paho.mqtt.client
import serial
import serial.tools.list_ports

from io_threads.backend_thread import BackendDataThread
from io_threads.arduino_thread import ArduinoDataThread

MACHINE_ID = 1 # unique machine identifier
MACHINE_SERIAL_PORT = "/dev/ttyUSB0" # serial port that is connected to the Arduino
MACHINE_BAUD_RATE = 9600 # baud rate used by the Arduino

def connect_serial() -> serial.Serial:
    # try to connect to the serial interface of the Arduino
    try:
        serial_client = serial.Serial(MACHINE_SERIAL_PORT, MACHINE_BAUD_RATE)
    except serial.serialutil.SerialException:
        print(f"Serial port {MACHINE_SERIAL_PORT} cannot be reached!")

        # print list of available ports for debugging
        print("Available ports:")
        print([str(port) for port in serial.tools.list_ports.comports()])
        sys.exit(1)

    # wait for the Arduino to reset
    time.sleep(5)

    print(f"Connected to Arduino via {MACHINE_SERIAL_PORT}")

    return serial_client

MQTT_BROKER = "broker.mqttdashboard.com" # broker that handles the MQTT messages
MQTT_PORT = 1883
MQTT_BASE_TOPIC = f"THM/drinkMachine/machine/{MACHINE_ID}"
MQTT_SEND_TOPIC = f"{MQTT_BASE_TOPIC}/toBackend" # topic used to send info/error messages to the backend
MQTT_RECEIVE_TOPIC = f"{MQTT_BASE_TOPIC}/fromBackend" # topic used to send config/order/led messages to the Arduino
MQTT_CLIENT_ID = f"python-mqtt-bridge-{MACHINE_ID}" # used by the broker to identify this machine

def connect_mqtt() -> paho.mqtt.client.Client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker: '{MQTT_BROKER}:{MQTT_PORT}'")
            print(f"The client ID of this MQTT client is: '{MQTT_CLIENT_ID}'")
        else:
            print(f"Failed to connect to the MQTT broker (return code: {rc})!")
            sys.exit(rc)

    # try to connect to the MQTT broker
    mqtt_client = paho.mqtt.client.Client(MQTT_CLIENT_ID)
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
    return mqtt_client

def run():
    # setup connections
    serial_client = connect_serial()
    mqtt_client = connect_mqtt()

    # start thread for handling incoming MQTT messages
    from_backend_thread = BackendDataThread(mqtt_client, serial_client, MQTT_RECEIVE_TOPIC)
    from_backend_thread.daemon = True # exit when main thread stops
    from_backend_thread.start()

    # start thread for handling serial input
    to_backend_thread = ArduinoDataThread(mqtt_client, serial_client, MQTT_SEND_TOPIC)
    to_backend_thread.daemon = True # exit when main thread stops
    to_backend_thread.start()

    try:
        # do nothing in main thread
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        print("Bridge stopped")

if __name__ == "__main__":
    run()