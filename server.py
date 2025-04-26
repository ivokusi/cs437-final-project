from flask import Flask, request
import time 
import json
import threading

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import gpiozero

class Pot:

	def __init__(self):
		spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
		cs = digitalio.DigitalInOut(board.D5)
		mcp = MCP.MCP3008(spi, cs)
		self.water_level = AnalogIn(mcp, MCP.P0)
		self.light = AnalogIn(mcp, MCP.P1)
		self.soil_moisture = AnalogIn(mcp, MCP.P2)
		self.water_pump = gpiozero.DigitalOutputDevice(4)
		self.water_pump.on()

		with open("config.json", "r") as file:
			config = json.load(file)
			self.water_level_threshold = config["water_level_threshold"]
			self.light_threshold = config["light_threshold"]
			self.soil_moisture_threshold = config["soil_moisture_threshold"]

	def _set_config(self, key, value):
		with open("config.json", "r") as file:
			config = json.load(file)
			config[key] = value

		with open("config.json", "w") as file:
			json.dump(config, file)

	def get_water_level(self):
		return { "value": self.water_level.value }

	def set_water_level_threshold(self):
		body = request.json
		threshold = body["threshold"]
		
		self._set_config("water_level_threshold", threshold)
		self.water_level_threshold = threshold

		return { "success": True }

	def get_light(self):
		return { "value": self.light.value }

	def set_light_threshold(self):
		body = request.json
		threshold = body["threshold"]
		
		self._set_config("light_threshold", threshold)
		self.light_threshold = threshold

		return { "success": True }

	def get_soil_moisture(self):
		return { "value": self.soil_moisture.value }

	def set_soil_moisture_threshold(self):
		body = request.json
		threshold = body["threshold"]
		
		self._set_config("soil_moisture_threshold", threshold)
		self.soil_moisture_threshold = threshold

		return { "success": True }

	def turn_on_water_pump(self):
		self.water_pump.off()

	def turn_off_water_pump(self):
		self.water_pump.on()

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
	app.run(host="0.0.0.0", port=8080)
