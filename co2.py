from time import sleep
from Adafruit_CCS811 import Adafruit_CCS811

ccs = Adafruit_CCS811()

# Wait for sensor to be ready
while not ccs.available():
    pass

while (1):
    if ccs.available():
        if not ccs.readData():
            print ("CO2: ", ccs.geteCO2(), "ppm, TVOC: ", ccs.getTVOC())
            
        else:
            print ("ERROR!")
            while (1):
                pass
    sleep(2)