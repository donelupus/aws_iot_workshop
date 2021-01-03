# Ratchet_Button Test Client
import sys
import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time


mqttc = AWSIoTMQTTClient("Ratchet_Button")

# Make sure you use your GGC end-point!!
mqttc.configureEndpoint("http://192.168.178.13",8883)
mqttc.configureCredentials("./RatchetWorkshop_Core_CA.pem","./Ratchet_Button.pem.key","./Ratchet_Button.pem.crt")

#Function to encode a payload into JSON
def json_encode(string):
    return json.dumps(string)

mqttc.json_encode=json_encode

message ={
   'message': "Hello from our Greengrass Device"
}

#Encoding into JSON
message = mqttc.json_encode(message)

mqttc.connect()

print("Connected to the Greengrass core!")

mqttc.publish("/ratchet", message, 0)

print("Message Published")
mqttc.disconnect()
time.sleep(2)
