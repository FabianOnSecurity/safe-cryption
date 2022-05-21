import numpy as np
from random import seed,randrange
import wave
#from pydub import AudioSegment

src = "Versuch 3.wav"
#srclen = len(src)
#if src[srclen-3:] == "mp3":
    #sound = AudioSegment.from_mp3(src)
    #src = src[:srclen-3]+"wav"
    #sound.export(src, format="wav")
#print(src)

Welle = wave.open(src,"r")
Wellenbytes = Welle.readframes(-1)
Wellenbits = np.frombuffer(Wellenbytes, dtype='int16')
Wellenliste = Wellenbits.tolist()
for i in range(0,18,1):
    while i in Wellenliste:
        Wellenliste.remove(i)
    while -i in Wellenliste:
        Wellenliste.remove(-i)

#print(Wellenliste)
def Soundgen(Wellenliste,keylen):
    x = 0
    for j in range(0,keylen//8,1):
        for l in range(0,16,1):
            y = Wellenliste[x]
            if y < 0 :
                y = -y
            if l == 0:
                Keyrunde = (y)
            else:
                Keyrunde = Keyrunde ^ y
            y = y % 128
            if x+y>= len(Wellenliste):
                x = j+1
            else:
                x = x + y
        value = str(hex(Keyrunde))[2:4]
        if len(value) < 2:
            seed()
            padding = randrange(1, 9)
            value = value + str(padding)
        if j == 0:
            final_key = value
        else:
            final_key = final_key + value
    print(final_key)
    print(len(final_key))
    return final_key

Soundgen(Wellenliste,256)
