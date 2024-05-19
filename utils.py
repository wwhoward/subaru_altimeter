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


def draw_text(*args, **kwargs): 
    # Erases text and draws screen
    display = kwargs.get("display", init_display())
    text = kwargs.get("text", "I finally got\nthis damn screen\nto work!")

    if display=="console": 
        print(text)
        return

    WHITE = (0xFF)
    BLACK = (0x00)
    
    text = kwargs.get("text", 
                        "I finally got\nthis damn screen\nto work! ")
                        
    display = kwargs.get("display", init_display())
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











