# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Be sure to check the learn guides for more usage information.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""

import digitalio
import board
import glob
from PIL import Image, ImageDraw, ImageOps, ImageFont
import time
from time import strftime, sleep
import cv2 as cv
import os
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import

def refresh_func():
    baseimage = Image.new("RGB", (width, height))
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(baseimage)
    

def display_tft(imageString):
    image = Image.open(imageString)
    # image = image.rotate(90)
    # image = image.crop((x, y, x + width, y + height))
    # image = ImageOps.fit(image, (135, 240), centering=(0.5,0.5))
    image.thumbnail([240, 135])

    x = 0
    y = 0
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    draw.text((x, y), "THIS IS A TEST", font=font, fill="#FFFFFF")

    # Display image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image, 90)


# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# pylint: disable=line-too-long
# Create the display:
# disp = st7789.ST7789(spi, rotation=90,                            # 2.0" ST7789
# disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=180,  # 1.3", 1.54" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, # 1.14" ST7789
# disp = hx8357.HX8357(spi, rotation=180,                           # 3.5" HX8357
# disp = st7735.ST7735R(spi, rotation=90,                           # 1.8" ST7735R
# disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
# disp = st7735.ST7735R(spi, rotation=90, bgr=True,                 # 0.96" MiniTFT ST7735R
# disp = ssd1351.SSD1351(spi, rotation=180,                         # 1.5" SSD1351
# disp = ssd1351.SSD1351(spi, height=96, y_offset=32, rotation=180, # 1.27" SSD1351
# disp = ssd1331.SSD1331(spi, rotation=180,                         # 0.96" SSD1331
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)
# pylint: enable=line-too-long

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
# if disp.rotation % 180 == 90:
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
# else:
width = disp.width  # we swap height/width to rotate it to landscape!
height = disp.height
image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image)

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Init PiTFT Image
folder_dir = "/home/pi/Documents/Interactive-Lab-Hub/Lab 2/memories"
images = glob.glob("memories/*.jpg")
currentImageIndex = 0
display_tft(images[currentImageIndex])

# SETUP WEBCAM
cam_port = 0
cam = cv.VideoCapture(cam_port)

print("Welcome MEMORY")
print("Enter 1 to search.")
print("Enter 2 to browse.")
print(">>> ")

selection = input()

if (selection == '1'):
    found = False
    print("Please enter a year: ")
    user_input_year = input()
    for image_string in images:
        if user_input_year in image_string:
            display_tft(image_string)
            found = True
        else:
            print("Searching")
    if found == False:
        print("No memories for the year " + user_input_year + " found")
    elif found == True:
        print("Please enjoy your memory!")

elif (selection == '2'):
    refresh = False

    while True:
        ret, frame = cam.read()
        frame = cv.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv.INTER_AREA)
        cv.imshow('Input', frame)
        c = cv.waitKey(1)
        if c == 27:
            break

        if buttonA.value and buttonB.value:
            pass
        elif not buttonA.value and not buttonB.value:
            print("MEMORY SAVED!")
            print("Please enter the date (YYYYMMDD): ")
            input = input()
            cv.imwrite(os.path.join(folder_dir, input + '.jpg'), frame)
            images = glob.glob("memories/*.jpg")
        if buttonB.value and not buttonA.value:  # just button A pressed
            # print("BUTTON A")
            refresh = True
            if (currentImageIndex - 1) >= 0:
                currentImageIndex = currentImageIndex - 1
            else:
                currentImageIndex = len(images) - 1
        if buttonA.value and not buttonB.value:  # just button B pressed
            # print("BUTTON B")
            refresh = True
            if (currentImageIndex + 1) < len(images):
                currentImageIndex = currentImageIndex + 1
            else:
                currentImageIndex = 0

        # ACTIONS AFTER A DIRECTIONAL BUTTON IS PRESSED
        if refresh == True:
            print("Date of photo: " + images[currentImageIndex].removeprefix('memories/').removesuffix('.jpg'))
            refresh_func()
            refresh = False
        display_tft(images[currentImageIndex])