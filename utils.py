# Python utilities for the Subaru Altimiter project
# @author wwh willwhoward@gmail.com
# Spring 2024
# 
# Display: Adafriut SSD1680 monochrome e-ink
# GPS: 

import digitalio
import busio
import board
import adafruit_gps
import reverse_geocoder
from adafruit_epd.ssd1680 import Adafruit_SSD1680
from adafruit_epd.epd import Adafruit_EPD
from PIL import Image, ImageDraw, ImageFont


def init_display(*args, **kwargs): 
    is_console = kwargs.get("console", 0)
    if is_console: 
        return "console"
    spi = busio.SPI(board.SCK, 
                    MOSI = board.MOSI, 
                    MISO = board.MISO)
    ecs = digitalio.DigitalInOut(board.CE0)
    dc = digitalio.DigitalInOut(board.D22)
    srcs = None
    rst = digitalio.DigitalInOut(board.D27)
    busy = digitalio.DigitalInOut(board.D17)

    display = Adafruit_SSD1680(122, 250, spi, cs_pin=ecs,
                            dc_pin=dc, sramcs_pin=srcs, rst_pin=rst, busy_pin=busy)
    
    display.rotation=3
        
    return display

def print_multiline_string(*args, **kwargs): 
    # Erases text and draws screen
    display = kwargs.get("display", init_display())
    text = kwargs.get("text", "I finally got\nthis damn screen\nto work!")

    if display=="console": 
        print(text)
        return

    WHITE = (0xFF)
    BLACK = (0x00)
    
    image = Image.new("L", (display.width, display.height))
    draw=ImageDraw.Draw(image)
    fontsize=16
    font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)    
    
    # Set background
    draw.rectangle((0,0,display.width-1,display.height-1),fill=WHITE)

    # Draw text
    (font_width, font_height) = font.getsize(text)
    draw.multiline_text((10, 10), 
                       text, 
                       font=font, 
                       fill=BLACK)

    # Refresh screen
    display.image(image)
    display.display()
               
def init_gps(): 
    i2c = board.I2C()
    gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    gps.send_command(b"PMTK220,1000")

    return gps

def new_frame(display, dat: dict) -> None: 
    
    # Erases text and draws screen
    if display=="console": 
        print(text)
        return

    WHITE = (0xFF)
    GREY  = (0x88)
    BLACK = (0x00)
    
    image = Image.new("L", (display.width, display.height))
    draw=ImageDraw.Draw(image)

    # Set background (seems a little expensive to do this every time, 
    #   but it's going once every three minutes... )
    draw.rectangle((0,0,display.width-1,display.height-1),fill=WHITE)

    # Draw lines

    # Draw text
    # Altitude
    altitude_str = "{}ft ASL".format(dat["altitude"]//.3048)
    font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 21)
    (text_width, text_height) = font.getsize(altitude_str)
    draw.text((0,0), altitude_str, font=font, fill=BLACK)
    draw.line([(0, text_height+3), (text_width+3, text_height+3)], fill=BLACK, width=1)
    draw.line([(text_width+3, text_height+3), (text_width+3, 0)], fill=BLACK, width=1)


    # What county are we in? 
    geocode = reverse_geocoder.search((dat["latitude"], dat["longitude"]))[0]
    if "County" in geocode["admin2"]: 
        location_str = geocode["admin2"].split(" ")[0]
    else: 
        location_str = geocode["admin2"]
    font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)    
    (text_width, text_height) = font.getsize(location_str)
    draw.text((0, 122-text_height), location_str, font=font, fill=BLACK)
    draw.line([(0, 122-text_height-3), (250, 122-text_height-3)], fill=BLACK, width=1)    

    # Time
    time_str = "{:02}:{:02}:{:02}z".format(
            dat["UTC"].tm_hour, 
            dat["UTC"].tm_min, 
            dat["UTC"].tm_sec, 
            )
    font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    (text_width, text_height) = font.getsize(time_str)
    draw.text((250-text_width, 122-text_height), time_str, font=font, fill=BLACK)
    
    # breakpoint()
    # frog=duck
    # Refresh screen
    display.image(image)
    display.display()








