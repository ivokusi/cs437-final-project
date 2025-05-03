from threading import Thread
import time

def water_plant(Pot):
    while (1):
        Pot.turn_on_water_pump()
        
        while (1):
            print(Pot.get_soil_moisture()["value"], Pot.soil_moisture_threshold)
            if Pot.get_water_level()["value"] < Pot.water_level_threshold:
                break
            if Pot.get_soil_moisture()["value"] < Pot.soil_moisture_threshold:
                break

            time.sleep(1)

        Pot.turn_off_water_pump()
        # time.sleep(60 * 60)
        time.sleep(5)

def start_auto_watering(Pot):
    thread = Thread(target=water_plant, args=(Pot, ))
    thread.daemon = True
    thread.start()