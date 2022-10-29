flite -voice slt -t "When you are in the sun and feel warm, that warm feeling is orange. Do you want to feel it?" 

arecord -D hw:1,0 -f cd -c1 -r 44100 -d 2 -t wav response.wav
python3 test_words.py response.wav