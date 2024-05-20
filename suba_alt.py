# Main function for the subaru altimeter project
# Objective is to have a module capable of reading from a GPS
# and printing to a display
# @author wwh willwhoward@gmail.com
# 
# Processor: raspberry-pi zero w
# Display: Adafruit SSD1680 monochrome e-ink 
# GPS: Adafruit Mini GPS PA1010D (self-contained GPS and antenna)

# Imports (display)
import digitalio
import busio
import board
from adafruit_epd.ssd1680 import Adafruit_SSD1680
from adafruit_epd.epd import Adafruit_EPD
from PIL import Image, ImageDraw, ImageFont
from subaru_altimeter import utils

# (GPS)
import time
import adafruit_gps

# Constants
update_interval = 3.0*60 # 3 minutes, recommended display refresh interval

# Initialize devices
# display = utils.init_display(console=True)
display = utils.init_display()
gps = utils.init_gps()
gps.update() # Call update to fill the object

# Initialize data dictionary
dat = {}
dat["altitude"] = -1
dat["latitude"] = -1
dat["longitude"] = -1
dat["UTC"] = gps.timestamp_utc


# Main loop
last_print = time.monotonic() - update_interval # So that we don't have to wait for first update
while True: 
    gps.update()
    current = time.monotonic()

    if current - last_print >= update_interval: 
        last_print = current 

        if gps.has_fix: 
            if gps.altitude_m is not None: 
                dat["altitude"] = gps.altitude_m

            if (gps.latitude is not None) and (gps.longitude is not None): 
                dat["latitude"] = gps.latitude
                dat["longitude"] = gps.longitude

            dat["UTC"] = gps.timestamp_utc

            # Print to display
            # utils.new_frame(dat)
        # else:            
        #     print_string = "NO FIX\nNO FIX\nNO FIX\nNO FIX" # Default screen text
        #     utils.print_multiline_string(display=display, text=print_string)
        utils.new_frame(display, dat)

        break






        





































