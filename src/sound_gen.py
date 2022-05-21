import numpy as np
from random import seed,randrange
import wave
#from pydub import AudioSegment

def prepare(src):
    #srclen = len(src)
    #if src[srclen-3:] == "mp3":
        #sound = AudioSegment.from_mp3(src)
        #src = src[:srclen-3]+"wav"
        #sound.export(src, format="wav")
    craze = wave.open(src,"r")
    crazebytes = craze.readframes(-1)
    crazebits = np.frombuffer(crazebytes, dtype='int16')
    crazelist = crazebits.tolist()
    for i in range(0,18,1):
        while i in crazelist:
            crazelist.remove(i)
        while -i in crazelist:
            crazelist.remove(-i)
    return crazelist

def Soundgen(crazelist,keylen):
    x = 0
    for j in range(0,keylen//8,1):
        for l in range(0,16,1):
            y = crazelist[x]
            if y < 0 :
                y = -y
            if l == 0:
                Keyround = (y)
            else:
                Keyround = Keyround ^ y
            y = y % 128
            if x+y>= len(crazelist):
                x = j+1
            else:
                x = x + y
        value = str(hex(Keyround))[2:4]
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


src = "Versuch 3.wav"
crazelist = prepare(src)
Soundgen(crazelist,256)
