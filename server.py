from flask import Flask, request
from flask_cors import CORS
import time 
import json
import threading
from Pot import Pot
from stream import start_streaming
from auto import start_auto_watering
from dotenv import load_dotenv
import requests
import os

load_dotenv()
LAMBDA_ENDPOINT = os.getenv("LAMBDA_ENDPOINT")

pot = Pot()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/water-level", methods=["GET"])
def get_water_level():
	return pot.get_water_level()

@app.route("/set-water-level", methods=["POST"])
def set_water_level_threshold():
	return pot.set_water_level_threshold()

@app.route("/water_level-threshold", methods=["GET"])
def get_water_level_threshold():
	return pot.get_water_level_threshold()

@app.route("/light", methods=["GET"])
def get_light():
	return pot.get_light()

@app.route("/set-light", methods=["POST"])
def set_light_threshold():
	return pot.set_light_threshold()

@app.route("/light-threshold", methods=["GET"])
def get_light_threshold():
	return pot.get_light_threshold()

@app.route("/soil-moisture", methods=["GET"])
def get_soil_moisture():
	return pot.get_soil_moisture()

@app.route("/set-soil-moisture", methods=["POST"])
def set_soil_moisture_threshold():
	return pot.set_soil_moisture_threshold()

@app.route("/soil_moisture-threshold", methods=["GET"])
def get_soil_moisture_threshold():
	return pot.get_soil_moisture_threshold()

@app.route("/water-plant", methods=["POST"])
def water_plant():
	data = request.json
	
	t = data["time"] # time in seconds

	# Turn on water pump
	pot.turn_on_water_pump()

	while t > 0:
	
		# Check for water level
		print(pot.get_water_level()["value"], pot.water_level_threshold)
		if pot.get_water_level()["value"] < pot.water_level_threshold:
			pot.turn_off_water_pump()
			return { "error": "Water level is too low" }
			
		# Check for soil moisture 
		print(pot.get_soil_moisture()["value"], pot.soil_moisture_threshold)
		if pot.get_soil_moisture()["value"] < pot.soil_moisture_threshold:
			pot.turn_off_water_pump()
			return { "error": "Soil moisture is too high" }
		
		time.sleep(0.5)
		t -= 0.5

	pot.turn_off_water_pump()

	return { "success": True }

@app.route("/historic", methods=["GET"])
def get_historic():
	return requests.get(LAMBDA_ENDPOINT + "/historic").json()

if __name__ == "__main__":
	start_streaming(pot)
	# start_auto_watering(pot)
	app.run(host="0.0.0.0", port=8080)
