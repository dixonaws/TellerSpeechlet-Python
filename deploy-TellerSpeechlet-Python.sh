#!/bin/bash

# create the Lambda deployment package -- just a zip file
zip TellerSpeechlet-deployment.zip TellerSpeechlet-Python.py

# publish the code to Lambda (the function must already exist)
aws --profile dixonaws@amazon.com --region us-east-1 lambda update-function-code --function-name TellerSpeechlet-Python --zip-file fileb://TellerSpeechlet-deployment.zip --publish
