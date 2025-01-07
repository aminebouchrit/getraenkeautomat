import json
from paho.mqtt import client as mqtt_client

broker = 'broker.mqttdashboard.com'
port = 1883
topic = "thm/drinkMachine/server/"
#generate client ID with pub prefix
client_id = f'python-mqtt-server'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker: '" + broker + "' on topic: '" + topic + "'\n")
        else:
            print("Failed to connect, return code %d\n", rc)
            exit(rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        if not is_valid_json(msg.payload.decode()):
           print("invalid message discarded\n")
           #print one new line to differentiate messages
           return
        print("valid json message subscribed")

    client.subscribe(topic)
    client.on_message = on_message

def is_valid_json(input):
    try:
        data = json.loads(input)
    except:
        return False     
    return True

def run():
    client = connect_mqtt()
    subscribe(client)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("connection closed")

if __name__ == "__main__":
    run()
