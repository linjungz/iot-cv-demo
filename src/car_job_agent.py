#!/usr/bin/python3
# car.py
# -- This is a demo program for AWS IoT Job and OTA
# -- It simulates a car that's connected to AWS IoT Core and use Job for OTA
# Author: Randy Lin

import json
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTThingJobsClient
from AWSIoTPythonSDK.core.jobs.thingJobManager import jobExecutionTopicType
from AWSIoTPythonSDK.core.jobs.thingJobManager import jobExecutionTopicReplyType
from AWSIoTPythonSDK.core.jobs.thingJobManager import jobExecutionStatus
import configparser
import random
import time
import logging
import wget

logging.basicConfig(level = logging.INFO)

#Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

#Setup MQTT client and security certificates
jobc = AWSIoTMQTTThingJobsClient('Car1', 'Car1')
jobc.configureEndpoint(
  config['Endpoints']['BJS_IOT_ENDPOINT'],
  int(config['Endpoints']['BJS_IOT_ENDPOINT_PORT'])
)
jobc.configureCredentials(
  config['Certs']['ROOT_CA'],
  config['Certs']['CAR_1_PRIVATE_KEY'],
  config['Certs']['CAR_1_CERT']
)

#Connect to IoT Core
jobc.connect()
print('Job Client Connected to IoT Core')

def execucte_job(payloadDict):
  if 'execution' in payloadDict:
    operation = payloadDict['execution']['jobDocument']['operation']
    jobId = payloadDict['execution']['jobId']

    if operation == 'updateFirmware':
      #Process Firmware Update
      firmware_url = payloadDict['execution']['jobDocument']['firmware_url']
      print('Start to download firmware...')
      name = 'car_firmware_' + str(time.time())
      wget.download(firmware_url, name)
      print("\n Download completed: " + name)
      print("Writing firmware to Flash memory and restart...")
      input("Now the job is in progress. Press Enter to complete the job")
      jobc.sendJobsUpdate(jobId, jobExecutionStatus.JOB_EXECUTION_SUCCEEDED)
      print('Job completed successfully.')
  else:
    print("No pending job for execution.")

#Callback: Job Notify Next
def job_notify_next_callback(client, userdata, message):
    print("Got Job Notification")
    payloadDict = json.loads(message.payload.decode('utf-8').replace("'", '"'))
    print(json.dumps(payloadDict, indent=4))
    if 'execution' in payloadDict:
      jobc.sendJobsStartNext()

#Callback: Start Next Job
def job_start_next_successfully_in_progess(client, userdata, message):
    print("Check if there's any pending job.")
    payloadDict = json.loads(message.payload.decode('utf-8').replace("'", '"'))
    print(json.dumps(payloadDict, indent=4))
    execucte_job(payloadDict)



jobc.createJobSubscription(job_notify_next_callback, jobExecutionTopicType.JOB_NOTIFY_NEXT_TOPIC)
print('Created Job Subscription for JOB NOTIFY NEXT')
jobc.createJobSubscription(job_start_next_successfully_in_progess, jobExecutionTopicType.JOB_START_NEXT_TOPIC, jobExecutionTopicReplyType.JOB_ACCEPTED_REPLY_TYPE)
jobc.sendJobsStartNext()

while True:
  time.sleep(1)
