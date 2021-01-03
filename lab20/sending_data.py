#!/usr/bin/python

# Lab 20 - Sending Analytics Data
# Make sure your host and region are correct.

import sys
import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time
from random import randint

#Setup our MQTT client and security certificates
#Make sure your certificate names match what you downloaded from AWS IoT

mqttc = AWSIoTMQTTClient("1234")

#Use the endpoint from the settings page in the IoT console
mqttc.configureEndpoint("data.iot.eu-central-1.amazonaws.com",8883)
mqttc.configureCredentials("./rootCA.pem","./privateKey.pem","./certificate.pem")

#Function to encode a payload into JSON
def json_encode(string):
        return json.dumps(string)

mqttc.json_encode=json_encode

#Setup a temp counter
temp = 0

#This sends our test message to the iot topic, sends a random temperature
#value and the correct unit of measurement.
def send():
    global temp
    message ={
        'temp': temp,
        'unit' : 'F'
    }
    temp = randint(0, 100)
    message = mqttc.json_encode(message)
    mqttc.publish("iot", message, 0)
    print "Message Published"

#Connect to the gateway
mqttc.connect()
print "Connected"

#Loop until terminated
while True:
    send()
    time.sleep(5)

mqttc.disconnect()

#To check and see if your message was published to the message broker go to the MQTT Client and subscribe to the iot topic and you should see your JSON Payload
