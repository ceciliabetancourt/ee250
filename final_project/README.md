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
