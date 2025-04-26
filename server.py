from flask import Flask, request
import time 
import json
import threading
from Pot import Pot
from stream import start_streaming
import json

pot = Pot()

app = Flask(__name__)

@app.route("/water-level", methods=["GET"])
def get_water_level():
	return pot.get_water_level()

@app.route("/set-water-level", methods=["POST"])
def set_water_level_threshold():
	return pot.set_water_level_threshold()

@app.route("/light", methods=["GET"])
def get_light():
	return pot.get_light()

@app.route("/set-light", methods=["POST"])
def set_light_threshold():
	return pot.set_light_threshold()

@app.route("/soil-moisture", methods=["GET"])
def get_soil_moisture():
	return pot.get_soil_moisture()

@app.route("/set-soil-moisture", methods=["POST"])
def set_soil_moisture_threshold():
	return pot.set_soil_moisture_threshold()

@app.route("/water-plant", methods=["POST"])
def post_water_plant():
	data = request.json
	
	t = data["time"] # time in seconds

	# Turn on water pump
	pot.turn_on_water_pump()

	while t > 0:
	
		# Check for water level
		if pot.get_water_level()["value"] < pot.water_level_threshold:
			pot.turn_off_water_pump()
			return { "error": "Water level is too low" }
			
		# Check for soil moisture 
		if pot.get_soil_moisture()["value"] < pot.soil_moisture_threshold:
			pot.turn_off_water_pump()
			return { "error": "Soil moisture is too high" }
		
		time.sleep(0.5)
		t -= 0.5

	pot.turn_off_water_pump()

	return { "success": True }

if __name__ == "__main__":
	start_streaming()
	app.run(host="0.0.0.0", port=8080)
