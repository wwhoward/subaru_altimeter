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

# Main loop
last_print = time.monotonic() - update_interval # So that we don't have to wait for first update
while True: 
    gps.update()
    current = time.monotonic()
    if current - last_print >= update_interval: 
        last_print = current 
        print_string = "NO FIX\nNO FIX\nNO FIX\nNO FIX" # Default screen text

        if gps.has_fix: 
            print_string = ""
            # Timestamp so we know when the last update was
            print_string += "UTC: {}/{}/{} {:02}:{:02}:{:02}\n".format(
                            gps.timestamp_utc.tm_mon, 
                            gps.timestamp_utc.tm_mday, 
                            gps.timestamp_utc.tm_year, 
                            gps.timestamp_utc.tm_hour, 
                            gps.timestamp_utc.tm_min, 
                            gps.timestamp_utc.tm_sec,
                            )

            # Elevation above sea level
            print_string += ("{}ft ASL\n".format(gps.altitude_m//.3048) if gps.altitude_m is not None
                            else "NO ALTITUDE\n")

            # Which US County/State
            print_string += "TODO ADD COUNTY\n"

            # ???
            print_string += "TODO Add something!"

        # Print to display
        utils.draw_text(display=display, text=print_string)
        break






        





































