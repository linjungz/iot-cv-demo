#!/usr/bin/python3
# -- This is a demo program for AWS IoT MQTT Topic
# -- It simulates sensors from car that's connected to AWS IoT Core and publish sensor data to a specific MQTT topic
# Author: Randy Lin

import json
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import random
import time

logging.basicConfig(level = logging.INFO)

#Setup MQTT client and security certificates
mqttc = AWSIoTMQTTClient("MyIoTDevice") 
mqttc.configureEndpoint("ChangeToYourEndpoint.ats.iot.cn-north-1.amazonaws.com.cn",8883)

mqttc.configureCredentials(
  './root-CA.crt',
  './MyIoTDevice.private.key',
  './MyIoTDevice.cert.pem'
)

#Connect to IoT Core
mqttc.connect()
logging.info('MQTT Client Connected to IoT Core')

#Send sensor data to IoT Core infinitly

#Sensor data is randomized between 20 to 40
temp_val_min = 20
temp_val_max = 40
lon = 39.09972
lat = -94.57853
pre =111
rpm = 2216
speed = 18
bat = 12.3
while True:
  temp_val = "{0:.1f}".format(random.uniform(temp_val_min, temp_val_max))
  lon = lon + (random.randrange(-1,2,1) * float(format(random.random()* .001,'.5f')))
  lat = lat + (random.randrange(-1,2,1) * float(format(random.random()* .001,'.5f')))
  pre = pre + int(random.randrange(-1,2,1) *random.random()* 5)
  rpm = rpm + int(random.randrange(-1,2,1) *random.random()* 10)
  speed = speed + int(random.randrange(-1,2,1) *random.random()*2)
  bat = bat + float(random.randrange(-1,2,1) * float(format(random.random()* .1,'.1f')))
  payload = {
      'name' : 'car1',
      'temperature' : temp_val,
      'location': "%s, %s" % (lon,lat),
      'geoJSON': {
        'type': "Point",
        'coordinates':[
            "%s" % (lon),
            "%s" % (lat)
        ]},
      'pressure': pre,
      'rpm':rpm,
      'speed' : speed,
      'battery': bat,
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
