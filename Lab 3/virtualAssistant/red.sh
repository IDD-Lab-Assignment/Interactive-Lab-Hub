flite -voice slt -t  "If you have ever had a sunburn, felt embarrassed and blushed, those feelings are red. Do you want to feel it?"

arecord -D hw:1,0 -f cd -c1 -r 44100 -d 2 -t wav response.wav
python3 test_words.py response.wav