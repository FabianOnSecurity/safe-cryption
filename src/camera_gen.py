import cv2
import time
from PIL import Image
from random import seed,randrange
from os import remove

class camera_key_gen():

    def webcam_image():
        video = cv2.VideoCapture(0)     
        check, frame = video.read()
        time_string = time.strftime("%H%M%S")
        file_name = f"Key_Gen_File_{time_string}.jpg"
        showPic = cv2.imwrite(file_name,frame)
        video.release()
        cv2.destroyAllWindows
        return file_name

    def check_size(filename):
        image = Image.open(filename)
        width, height = image.size
        img_size = width*height
        if img_size < 100000:
            print("ImageSize too small.")
            exit()
        return img_size

    def return_pixeldata(filename):
        image = Image.open(filename, "r")
        pixel_values = list(image.getdata())
        return pixel_values

    def XOR(a,b):
        return a ^ b
    
    def calculate_xor_image(filename, key_size):
        if key_size == 128:
            block_rounds = 16
        elif key_size == 192:
            block_rounds = 24
        elif key_size == 256:
            block_rounds = 32
        else:
            print("Keysize not supported!")
            exit()

        final_key = ""
        pxl = camera_key_gen.return_pixeldata(filename)
        img_size = camera_key_gen.check_size(filename)
        values_per_round = img_size // block_rounds
        for i in range(0,block_rounds):
            for j in range(0,values_per_round):
                for k in range(0,3):
                    if k == 0:
                        pixel_triple = pxl[i*values_per_round+j][k]
                    else:
                        pixel_triple = pxl[i*values_per_round+j][k] + pixel_triple
                
                if j == 0:
                    block_value = pixel_triple
                else:
                    block_value = camera_key_gen.XOR(block_value,pixel_triple)

            value = str(hex(block_value))[2:4]
            if len(value) < 2:
                seed()
                padding = randrange(1,9)
                value = value + str(padding)

            final_key = final_key + value

        remove(filename)
        return final_key
