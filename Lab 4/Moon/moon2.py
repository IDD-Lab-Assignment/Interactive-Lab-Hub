
###Not actual code for running, just testing###
import time
import board
import os
import RPi.GPIO as GPIO
import neopixel
from adafruit_seesaw import seesaw, rotaryio, digitalio
import adafruit_mpr121
import busio
from threading import Thread
import pygame
import adafruit_mpr121
import busio

# Setup Touch Sensor
i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

# Define Music

music_list = ["ToTheMoon.mp3","Kumru.mp3", "Height.mp3", "JokerAndQueen.mp3","OffMyFace.mp3","Sigh.mp3"]

# Function for Touch Sensor
def sensor_update_ind(init_ind):
    init_temp = init_ind
    # capacitive sensor 2 triggered - play previous song
    # Capacitive sensor 7 triggered - play the next song
    if not mpr121[2].value and not mpr121[7].value:
        return (init_ind, init_ind)
    elif mpr121[2].value and init_ind != 0:
        return (init_ind, init_ind - 1)
    elif mpr121[2].value and init_ind == 0:
        return (init_ind, 5)
    elif mpr121[7].value: 
        return (init_ind, init_ind + 1)
    else: return (init_ind, init_ind)



def lights():
    # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
    # NeoPixels must be connected to D10, D12, D18 or D21 to work.
    pixel_pin = board.D21

    # The number of NeoPixels
    num_pixels = 30

    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
    ORDER = neopixel.GRB

    pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
    )

    my_seesaw = seesaw.Seesaw(board.I2C(), addr=0x36)

    seesaw_product = (my_seesaw.get_version() >> 16) & 0xFFFF
    print("Found product {}".format(seesaw_product))
    if seesaw_product != 4991:
        print("Wrong firmware loaded?  Expected 4991")

    my_seesaw.pin_mode(24, my_seesaw.INPUT_PULLUP)
    button = digitalio.DigitalIO(my_seesaw, 24)
    button_held = False

    encoder = rotaryio.IncrementalEncoder(my_seesaw)
    last_position = 0
    lights = 0

    blank = ((0,0,0))
    white = ((253,253,253))
    yellow = ((253,80,0))
    orange = ((153,110,0))

    colour_val = 0
    last_position = 0
    while True:
        position = encoder.position

        if position > last_position:
            last_position = position
            print("Position: {}".format(position))
            if lights < 30:
                lights += 1
            else:
                if colour_val == 0:
                    colour_val += 1
                elif colour_val == 1:
                    colour_val +=1
                else:
                    colour_val = 0
        elif position < last_position:
            last_position = position
            print("Position: {}".format(position))
            lights -= 1

        else:
            lights = lights
        
        if colour_val == 1:
            colour = white
        elif colour_val == 2:
            colour = yellow
        else:
            colour = orange

        for i in range(30):
            if i in range(lights):
                pixels[i] = colour
            else:
                pixels[i] = blank

        pixels.show()

    def music():
        i2c = busio.I2C(board.SCL, board.SDA)

        mpr121 = adafruit_mpr121.MPR121(i2c)

        music_list = ["ToTheMoon.mp3","Kumru.mp3", "Height.mp3", "JokerAndQueen.mp3","OffMyFace.mp3","Sigh.mp3"]
        pygame.mixer.init()

    def play_music(index):
        pygame.mixer.music.load(music_list[index])
        pygame.mixer.music.play()
        
    def sensor_update_ind(init_ind):
        init_temp = init_ind
        # capacitive sensor 7 triggered - play previous song
        # Capacitive sensor 9 triggered - play the next song
        if not mpr121[7].value and not mpr121[9].value:
            return (init_ind, init_ind)
        elif mpr121[7].value and init_ind != 0:
            return (init_ind, init_ind - 1)
        elif mpr121[7].value and init_ind == 0:
            return (init_ind, 5)
        elif mpr121[9].value: 
            return (init_ind, init_ind + 1)
        else: return (init_ind, init_ind)

    def ind_six(num):
        return num % 6
    
    MUSIC_END = pygame.USEREVENT+1
    pygame.init()

    pygame.mixer.music.set_endevent(MUSIC_END)
    temp = 5
    curr_ind= 0
    pygame.mixer.music.load(music_list[curr_ind])
    pygame.mixer.music.play(ind_six(curr_ind))
    
    while True:
        
        curr_ind, next_ind = sensor_update_ind(curr_ind)
        if curr_ind != next_ind:
            pygame.mixer.music.stop()
            play_music(ind_six(next_ind))
            time.sleep(2)
            curr_ind = next_ind

        # check for stop
        #if one song ends, plays the next
        for event in pygame.event.get():
            if event.type == MUSIC_END:
                curr_index += 1
                curr_index %= len(music_list)
                pygame.mixer.music.load(music_list[curr_index])
                pygame.mixer.music.play()


LightThread = Thread(target=lights())
LightThread.start()

MusicThread = Thread(target=music())
MusicThread.start()

LightThread.join()
MusicThread.join()
