flite -voice slt -t "The smoothness and suppleness of the grass and leaves feel like green; green feels like life. Do you want to feel it?" 

arecord -D hw:1,0 -f cd -c1 -r 44100 -d 2 -t wav response.wav
python3 test_words.py response.wav