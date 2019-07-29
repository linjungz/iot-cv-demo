#!/usr/bin/python3
# -- This is a demo program for AWS IoT MQTT Topic
# -- It simulates sensors from car that's connected to AWS IoT Core and publish sensor data to a specific MQTT topic
# Author: Randy Lin

import json
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import configparser
import logging
import random
import time

logging.basicConfig(level = logging.INFO)

#Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

#Setup MQTT client and security certificates
mqttc = AWSIoTMQTTClient("car1") 
mqttc.configureEndpoint(
  config['Endpoints']['BJS_IOT_ENDPOINT'],
  int(config['Endpoints']['BJS_IOT_ENDPOINT_PORT'])
)

mqttc.configureCredentials(
  './AmazonRootCA1.pem',
  './car-private.pem.key',
  './car-certificate.pem.crt'
)

#Connect to IoT Core
mqttc.connect()
logging.info('MQTT Client Connected to IoT Core')

#Send sensor data to IoT Core infinitly

#Sensor data is randomized between 20 to 40
temp_val_min = 20
temp_val_max = 40

while True:
  temp_val = "{0:.1f}".format(random.uniform(temp_val_min, temp_val_max))
  #TODO: Add more telemetry data such as speed, fuel and etc
  payload = {
      'name' : 'car1',
      'temperature' : temp_val,
      'timestamp' : time.time()
  }
  result = mqttc.publish(
    'connectedcar/telemetry/car1', 
    json.dumps(payload),
    0
  )
  logging.info(json.dumps(payload))
  if result == False:
    logging.error('Failed to publish message.')

  time.sleep(5)
