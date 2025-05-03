
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import gpiozero
import json

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
		value = self.water_level.value
		status = "low" if value < self.water_level_threshold else "high"
		return { "value": value, "status": status }

	def set_water_level_threshold(self):
		threshold = self.water_level.value
		
		self._set_config("water_level_threshold", threshold)
		self.water_level_threshold = threshold

		return { "success": True }

	def get_water_level_threshold(self):
		return { "threshold": self.water_level_threshold }

	def get_light(self):
		value = self.light.value
		status = "dark" if value < self.light_threshold else "light"
		return { "value": value, "status": status }

	def set_light_threshold(self):
		threshold = self.light.value
		
		self._set_config("light_threshold", threshold)
		self.light_threshold = threshold

		return { "success": True }

	def get_light_threshold(self):
		return { "threshold": self.light_threshold }

	def get_soil_moisture(self):
		value = self.soil_moisture.value
		status = "dry" if value < self.soil_moisture_threshold else "wet"
		return { "value": value, "status": status }

	def set_soil_moisture_threshold(self):
		threshold = self.soil_moisture.value
		
		self._set_config("soil_moisture_threshold", threshold)
		self.soil_moisture_threshold = threshold

		return { "success": True }

	def get_soil_moisture_threshold(self):
		return { "threshold": self.soil_moisture_threshold }

	def turn_on_water_pump(self):
		self.water_pump.off()

	def turn_off_water_pump(self):
		self.water_pump.on()
