import json
import random
import sys
import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time

thingName = "ratchet-RaspberryPi"

mqttc = AWSIoTMQTTClient(thingName)

#Make sure you use the correct region!
mqttc.configureEndpoint("data.iot.eu-central-1.amazonaws.com",8883)
mqttc.configureCredentials("./rootCA.pem","./privateKey.pem","./certificate.pem")

#Function to encode a payload into JSON
def json_encode(string):
        return json.dumps(string)

mqttc.json_encode=json_encode

#This sends our test message to the iot topic
def send(message):
    mqttc.publish("data/"+thingName+"/bloodpressure", message, 0)
    print "Message Published"

#Connect to the gateway
mqttc.connect()
print "Connected"

# Generate normal blood pressure with a 0.995 probability
def getNormalBloodPressure():
    data = {}
    data['Systolic'] = random.randint(90, 120)
    data['Diastolic'] = random.randint(60, 80)
    data['BloodPressureLevel'] = 'NORMAL'
    return data

# Generate high blood pressure with probability 0.005
def getHighBloodPressure():
    data = {}
    data['Systolic'] = random.randint(130, 200)
    data['Diastolic'] = random.randint(90, 150)
    data['BloodPressureLevel'] = 'HIGH'
    return data

# Generate low blood pressure with probability 0.005
def getLowBloodPressure():
    data = {}
    data['Systolic'] = random.randint(50, 80)
    data['Diastolic'] = random.randint(30, 50)
    data['BloodPressureLevel'] = 'LOW'
    return data

while True:
    rnd = random.random()
    if (rnd < 0.005):
        data = json.dumps(getLowBloodPressure())
        print(data)
        send(data)
    elif (rnd > 0.995):
        data = json.dumps(getHighBloodPressure())
        print(data)
        send(data)
    else:
        data = json.dumps(getNormalBloodPressure())
        print(data)
        send(data)
    time.sleep(1)

mqttc.disconnect()

