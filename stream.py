from threading import Thread
from time import sleep
from dotenv import load_dotenv
import os
import requests

load_dotenv()
LAMBDA_ENDPOINT_STREAM = os.getenv("LAMBDA_ENDPOINT_STREAM")

def get_cur_data(pot):
    return {
        "id": 0,
        "data": {
            "water_level": pot.get_water_level(),
            "light": pot.get_light(),
            "soil_moisture": pot.get_soil_moisture(),
            "pump": 0
        }
    }

def send_data(data):
    try:
        res =  requests.post(LAMBDA_ENDPOINT_STREAM + "/prod/stream", json=data)
        if res.status_code == 200:
            return res.json()
        else:
            print(res)
            return None
    except:
        print("COULD NOT SEND DATA")

def stream_data(pot):
    while (1):
        data = get_cur_data(pot)
        send_data(data)
        sleep(60 * 5)


def start_streaming(Pot):
    thread = Thread(target=stream_data, args=(Pot, ))
    thread.daemon = True
    thread.start()