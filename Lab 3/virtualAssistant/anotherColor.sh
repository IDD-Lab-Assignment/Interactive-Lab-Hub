espeak -ven+f2 -k5 -s150 --stdout  "Alright! Ask me about another color then!" | aplay

xarecord -D hw:1,0 -f cd -c1 -r 16000 -d 2 -t wav response.wav
python3 test_words.py response.wav