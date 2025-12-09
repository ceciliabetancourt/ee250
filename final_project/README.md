# partner names – Cecilia Betancourt and Leire Lizarralde

# (1) instructions to compile and execute the code
1. Connect the GrovePi to the Raspberry Pi, and then connect the potentiometer to port A0 and the light sensor to port A1
2. After this has been done, ssh to the Raspberry Pi and download and run the 'rpi_pub.py' file
3. On a laptop, open a terminal and run the 'display_client.py' file
4. Open a second terminal and run the 'display_server.py' file
5. Open a third terminal, and run the following files in sequential order:
    - 'weather_api.py' (makes use of 'vm_sub.py', so the user does not need to run that file)
    - 'weather_prediction.py'
    Before doing so, ensure that 'model_training.py' –which is responsible for building and training our three ML models in one file– has been previously executed. This only needs to be done once.
6. Open the following HTTP link (http://127.0.0.1:5000/send_data) in a browser within the computer to view the output, and reload every time a new output is generated!

# (2) list of external libraries used
import paho.mqtt.client as mqtt
import requests
import json
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time
import sys
import grovepi
import threading
import os
from joblib import load

# (3) list of imports
pip3 install paho-mqtt
python3 -m venv myenv
source myenv/bin/activate
pip install requests pandas numpy scikit-learn matplotlib

# (4) ChatGPT promps
- for vm_sub.py
    “Can you please help me resolve this issue I’m having with my code? The following files, weather_prediction.py and weather_api.py, seem to work normally but they throw an error when calling for vm_sub.latest_city. No matter what, it seems like latest_city = None when we can see it updating on the published topic. What do you think this issue could be and what is a possible solution to address it?”
- for model_training.py
    “I currently have the following file for training a regression based model to predict the temperature for tomorrow based on the past 60 days of weather with a specific focus on the last 7. For my project, I need three different versions of this model based on three different cities (“Los Angeles”, “Madrid”, and “London”). How could I modify this file to build and train all three models at once for brevity?”
- for weather_prediction.py
    “How would I add code to load 3 ML models (joblib file type with model and scalar files separate) within a folder in a directory in python?”
- for 'display_server.py':
    "How can I add a branch of if-else statements that determine the background of the http website based on the value of the display_color variable?"

# (5) link to our youtube video
Link to our EE250 video! –> https://youtu.be/Krv5dTciWnk
