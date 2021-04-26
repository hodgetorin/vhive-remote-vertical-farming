# set up relays
from gpiozero import OutputDevice
import time
import sys

# devices specified by GPIO number
# gpiozero.OutputDevice(pin, *, active_high=True, initial_value=False, pin_factory=None)
air_pump = OutputDevice(18, False)
nutrient_pump = OutputDevice(23, False)
solenoid = OutputDevice(24, False)
l_board = OutputDevice(25, False)
motors = OutputDevice(4, False)

#function to toggle relay power
def TogglePower(relay):
    relay.toggle()

#TogglePower(air_pump)
        #time.sleep(1)
#TogglePower(motors)
        #time.sleep(1)
#TogglePower(l_board)
        #time.sleep(1)
#TogglePower(nutrient_pump)   
#TogglePower(solenoid)
#time.sleep(1)
#TogglePower(solenoid)
