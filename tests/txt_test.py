# Test writing test to display
# Subaru altimiter project
# @author wwh willwhoward@gmail.com

import digitalio
import busio
import board
from subaru_altimeter import utils
from PIL import Image,ImageDraw, ImageFont
from adafruit_epd.ssd1680 import Adafruit_SSD1680
from adafruit_epd.epd import Adafruit_EPD

WHITE = (0xFF)
BLACK = (0x00)

display = utils.init_display()
image = Image.new("L", (display.width, display.height))
draw=ImageDraw.Draw(image)
fontsize=24
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)
text = "I finally got this damn screen to work!"

# Set background color
draw.rectangle((0,0,display.width-1, display.height-1), fill=WHITE)

# Draw text
(font_width, font_height) = font.getsize(text)
draw.text((display.width//2-font_width//2, display.height//2-font_height//2), text, font=font, fill=BLACK)

display.image(image)
display.display()


