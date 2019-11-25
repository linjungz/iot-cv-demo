#!/usr/bin/python3
# light.py
# -- This is a demo program for AWS IoT Shadow
# -- It simulates a light that's connected to AWS IoT Core and use Shadow for status control
# Author: Randy Lin

import json
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import configparser
import random
import time

#Setup Shadow client and security certificates
shadowc = AWSIoTMQTTShadowClient('Light1')
shadowc.configureEndpoint("ChangeToYourEndpoint.ats.iot.cn-north-1.amazonaws.com.cn",8883)

shadowc.configureCredentials(
  './root-CA.crt',
  './MyIoTDevice.private.key',
  './MyIoTDevice.cert.pem'
)

#Initialize Device Status
device_state_color = 'white'
device_state_brightness = '30'

#Connect to IoT Core
shadowc.connect()
print('Shadow Client Connected to IoT Core')

#Create Device Shadow Handler with persistent subscription
deviceShadowHandler = shadowc.createShadowHandlerWithName('MyIoTDevice', True)

#Callback: Shadow Update
def shadow_update_callback(payload, responseStatus, token):
    if responseStatus == 'timeout':
        print(f'Shadow Update Request {token} time out!')
    if responseStatus == 'rejected':
        print(f'Shadow Update Request {token} rejected.')    
    if responseStatus == 'accepted':
        print(f'Shadow Update Request {token} accepted.')

#Callback: Shadow Get for Device Initialization
def shadow_get_init_callback(payload, responseStatus, token):
    global device_state_color
    global device_state_brightness

    if responseStatus == 'timeout':
        print(f'Shadow Get Request {token} time out!')

    if responseStatus == 'rejected':
        print(f'Shadow Get Request {token} rejected.')
        print('Maybe the Shadow is not created yet.')
    
    if responseStatus == 'accepted':
        print(f'Shadow Get Request {token} accepted.')
        payloadDict = json.loads(payload)
        print('Now Got Shadow and Use it for Device Initialization')
        print(json.dumps(payloadDict, indent=4))

        #Check if there's pending change
        if 'delta' in payloadDict['state']:
            print('Got pending change in shadow and will apply it to device first')
            print(json.dumps(payloadDict['state']['delta'], indent=4))
            if 'color' in payloadDict['state']['delta']:
                device_state_color = payloadDict['state']['delta']['color']
                print('Color -> ' + device_state_color)
                print('Pending change for color has been applied to device')
            if 'brightness' in payloadDict['state']['delta']:
                device_state_brightness = payloadDict['state']['delta']['brightness']
                print('Brightness -> ' + device_state_brightness)
                print('Pending change for brightness has been applied to device')
            input('Now you can check the shadow document in AWS Console before I update it. Press Enter to continue.')
        elif payloadDict['state'] == {} :
            print('Empty shadow. Need to initialize it.')
        else:
            print("There's no delta in Shadow, so report the initial state")
            device_state_color = payloadDict['state']['reported']['color']
            device_state_brightness = payloadDict['state']['reported']['brightness']

    #Report Current State to Shadow
    current_device_state = {
        "state": {
            "reported": {
                "color": device_state_color,
                "brightness": device_state_brightness
            },
            "desired" : None
        }
    }
    print(json.dumps(current_device_state, indent=4))
    deviceShadowHandler.shadowUpdate(json.dumps(current_device_state), shadow_update_callback, 5)
    print('Completed Device Initialization.')

    
#Callback: Shadow Delta
def shadow_delta_callback(payload, responseStatus, token):
    global device_state_color
    global device_state_brightness

    print('Got Delta in Shadow.')
    payloadDict = json.loads(payload)
    print(json.dumps(payloadDict, indent=4))
    if 'color' in payloadDict['state']:
        device_state_color = payloadDict['state']['color']
        print('Color -> ' + device_state_color)
        print('Pending change for color has been applied to device.')
    if 'brightness' in payloadDict['state']:
        device_state_brightness = payloadDict['state']['brightness']
        print('Brightness -> ' + device_state_brightness)
        print('Pending change for brightness has been applied to device')

    input('Now you can check the shadow document in AWS Console before I update it. Press Enter to continue.')

    #Report Current State to Shadow
    current_device_state = {
        "state": {
            "reported": {
                "color": device_state_color,
                "brightness": device_state_brightness
            },
            "desired" : None
        }
    }
    print('Report current status to shadow')
    deviceShadowHandler.shadowUpdate(json.dumps(current_device_state), shadow_update_callback, 5)

#Main
#Register Callback for Shadow Delta
deviceShadowHandler.shadowRegisterDeltaCallback(shadow_delta_callback)
print('Registered callback for delta')

#Power on the light and report status
print("Now turn on the light and start device initialization.")
deviceShadowHandler.shadowGet(shadow_get_init_callback, 5)

while True:
    time.sleep(1)