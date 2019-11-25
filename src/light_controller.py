#!/usr/bin/python3
# light_controller.py
# -- This is a demo program for AWS IoT Shadow
# -- It simulates a light controller that's connected to AWS IoT Core and use Shadow to control a light
# Author: Randy Lin

import json
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import configparser
import random
import time

#Setup Shadow client and security certificates
shadowc = AWSIoTMQTTShadowClient('Light1_controller')
shadowc.configureEndpoint("ChangeToYourEndpoint.ats.iot.cn-north-1.amazonaws.com.cn",8883)

shadowc.configureCredentials(
  './root-CA.crt',
  './MyIoTDevice.private.key',
  './MyIoTDevice.cert.pem'
)

#Connect to IoT Core
shadowc.connect()
print('Shadow Client Connected to IoT Core')

#Create Device Shadow Handler with persistent subscription
deviceShadowHandler = shadowc.createShadowHandlerWithName('MyIoTDevice', True)

#Callback: Shadow Update
def shadow_update_callback(payload, responseStatus, token):
    if responseStatus == 'timeout':
        print(f'Shadow Update Request {token} time out!')
    if responseStatus == 'accepted':
        print(f'Shadow Update Request {token} accepted.')
        payloadDict = json.loads(payload)
        print(payloadDict)
    if responseStatus == 'rejected':
        print(f'Shadow Update Request {token} rejected.')

print('Welcome to light controller')
color_to_change = input('What color to change? ')
brightness_to_change = input('What brightness to change? ')

desired_state = {'state': {'desired': {}}}
if color_to_change != "":
    desired_state['state']['desired']['color'] = color_to_change
if brightness_to_change != "":
    desired_state['state']['desired']['brightness'] = brightness_to_change
print(desired_state)

deviceShadowHandler.shadowUpdate(json.dumps(desired_state), shadow_update_callback, 5)
