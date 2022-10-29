## Music Feature of the installation ###

import time
import board
import os
import RPi.GPIO as GPIO
import pygame
import adafruit_mpr121
import busio

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

music_list = ["ToTheMoon.mp3","Sigh.mp3", "Kumru.mp3", "Height.mp3", "JokerAndQueen.mp3","OffMyFace.mp3"]
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
        return (init_ind, len(music_list))
    elif mpr121[9].value: 
        return (init_ind, init_ind + 1)
    else: return (init_ind, init_ind)

def ind_six(num):
    return num % len(music_list)
    


def main():

    MUSIC_END = pygame.USEREVENT+1

    pygame.init()

    pygame.mixer.music.set_endevent(MUSIC_END)
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
                curr_ind += 1
                curr_ind %= len(music_list)
                play_music(curr_ind)
            else: continue


if __name__ == "__main__":
    main()
