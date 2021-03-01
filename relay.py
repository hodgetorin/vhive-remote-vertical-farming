# set up relays
from gpiozero import Button, OutputDevice

# devices specified by GPIO number
air_pump = OutputDevice(18)
nutrient_pump = OutputDevice(23)
solenoid = OutputDevice(24)
l_board = OutputDevice(25)

# pressing button will toggle airpump power
button = Button(8)

#function to toggle relay power
def TogglePower(relay):
    toggle(relay)



while True:
    try:
        if button.is_pressed:
            TogglePower(air_pump)
    except KeyboardInterrupt:
        exit()
        

