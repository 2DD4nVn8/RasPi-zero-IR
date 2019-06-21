import IRmodule
import csv
import paho.mqtt.client as mqtt
import ast
import pandas as pd
from ast import literal_eval

MQTT_FILE = "/home/pi/WorkSpace/mqtt/mqtt.txt"
mqtt_broker = open(MQTT_FILE).read()
mqtt_dict = literal_eval(mqtt_broker)
MQTT_BROKER_ADDR = mqtt_dict['MQTT_BROKER_ADDR']
MQTT_BROKER_PORT = mqtt_dict['MQTT_BROKER_PORT']

SUB_TOPIC = "SmartHome/RemoteController/RecSignal"
PUB_TOPIC = "SmartHome/RemoteController/text"

filename = "/home/pi/WorkSpace/IR_sender/IR_recode.csv"

PUB_TEXT = 'If you want to recode IR-signal, Please send json message ! \nTOPIC is "SmartHome/RemoteController/RecSignal". element is room, id and key. '

print(PUB_TEXT)

def toCSV(room, controller, key):
    if room != None and controller != None and key != None :
        print("please send signal")
        signal = IRmodule.IR_controller("r")
        print()
        if len(signal) > 0 :
            df = pd.read_csv(filename, index_col = ["room","id","key"])
            print(df)
            df.loc[room, controller, key] = [signal]
            print(df)
            df.to_csv(filename, mode='w')
            
            print("recode success")
            print()
            pub_Message = 'recode success, data_len : ' + str(len(signal))
            mqtt_publisher.publish(PUB_TOPIC, pub_Message, qos=0)
            print("send")
            return  True
        else :
            pub_Message = 'error, data_len : ' + str(len(signal))
            mqtt_publisher.publish(PUB_TOPIC, pub_Message, qos=0)
            return False

    else :
        pub_Message = 'error, data_len : ' + str(len(signal))
        mqtt_publisher.publish(PUB_TOPIC, pub_Message, qos=0)
        return False

def onConnect(publisher, user_data, flags, response_code):
    print("response code: {0}".format(response_code))
    publisher.subscribe(SUB_TOPIC, 0)


def onMessage(publisher, user_data, msg):
    print("topic: " + msg.topic)
    print("subtopic " + msg.topic.split("/")[1])
    print("payload: " + str(msg.payload.decode('utf-8')))
    print(msg.payload)
    payload_DICT = ast.literal_eval(msg.payload.decode('utf-8'))

    toCSV(payload_DICT["room"], payload_DICT["id"], payload_DICT["key"])




if __name__ == '__main__':
    mqtt_subscriber = mqtt.Client(protocol=mqtt.MQTTv31)
    mqtt_subscriber.on_connect = onConnect
    mqtt_subscriber.on_message = onMessage
    mqtt_subscriber.connect(host=MQTT_BROKER_ADDR, port=MQTT_BROKER_PORT, keepalive=0)

    mqtt_publisher = mqtt.Client(protocol=mqtt.MQTTv31)
    mqtt_publisher.connect(host=MQTT_BROKER_ADDR, port=MQTT_BROKER_PORT, keepalive=0)
    
    mqtt_publisher.publish(PUB_TOPIC, PUB_TEXT, qos=0)


try:
    mqtt_subscriber.loop_forever()

except KeyboardInterrupt:
    None

