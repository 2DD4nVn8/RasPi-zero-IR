import IRmodule
import csv
import pandas as pd
import paho.mqtt.client as mqtt
import ast
from ast import literal_eval

MQTT_FILE = "/home/pi/WorkSpace/mqtt/mqtt.txt"
mqtt_broker = open(MQTT_FILE).read()
mqtt_dict = literal_eval(mqtt_broker)
MQTT_BROKER_ADDR = mqtt_dict['MQTT_BROKER_ADDR']
MQTT_BROKER_PORT = mqtt_dict['MQTT_BROKER_PORT']

SUB_TOPIC = "SmartHome/RemoteController/send"
PUB_TOPIC = "SmartHome/RemoteController/text"

filename = "/home/pi/WorkSpace/IR_sender/IR_recode.csv"

def onConnect(publisher, user_data, flags, response_code):
    print("response code: {0}".format(response_code))
    publisher.subscribe(SUB_TOPIC, 0)


def onMessage(publisher, user_data, msg):
    df = pd.read_csv(filename, index_col = ["room","id","key"])
    print("topic: " + msg.topic)
    print("subtopic " + msg.topic.split("/")[1])
    print("payload: " + str(msg.payload.decode('utf-8')))
    print(msg.payload)
    DICT = ast.literal_eval(msg.payload.decode('utf-8'))


    print(df)
    send_data = df.loc[(DICT["room"],DICT["id"],DICT["key"]),"signal"]
    print(send_data)
    print(type(send_data))

    IRmodule.IR_controller("w", block=send_data)

if __name__ == '__main__':
    mqtt_subscriber = mqtt.Client(protocol=mqtt.MQTTv31)
    mqtt_subscriber.on_connect = onConnect
    mqtt_subscriber.on_message = onMessage
    mqtt_subscriber.connect(host=MQTT_BROKER_ADDR, port=MQTT_BROKER_PORT, keepalive=0)

    mqtt_publisher = mqtt.Client(protocol=mqtt.MQTTv31)
    mqtt_publisher.connect(host=MQTT_BROKER_ADDR, port=MQTT_BROKER_PORT, keepalive=0)
    

try:
    mqtt_subscriber.loop_forever()

except KeyboardInterrupt:
    None

