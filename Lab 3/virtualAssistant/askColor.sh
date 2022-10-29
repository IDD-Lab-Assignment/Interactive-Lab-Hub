#from https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)
espeak -ven+f2 -k5 -s150 --stdout "What color would you like to learn today?" | aplay

#arecord -f cd -r 16000 -d 5 -t wav recorded.wav && sox recorded.wav recorded_mono.wav remix 1,2

arecord -D hw:1,0 -f cd -c1 -r 16000 -d 2 -t wav response.wav
python3 test_words.py response.wav