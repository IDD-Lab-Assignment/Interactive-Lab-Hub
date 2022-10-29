espeak -ven+f2 -k5 -s150 --stdout  "Yellow is like the warmth of sunlight in springtime, like the excitement without being loud or angry. Do you want to feel it?" | aplay

arecord -D hw:1,0 -f cd -c1 -r 16000 -d 2 -t wav response.wav
python3 test_words.py response.wav