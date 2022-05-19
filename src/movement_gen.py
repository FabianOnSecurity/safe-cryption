from time import sleep, time

#----------Hide PYGAME STRING----------#
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import struct
import random

class movement_generator():
    def random_movement_value(movement_time, key_length):
        screen = pygame.display.set_mode((999, 999))

        def float_xor(a, b):
            rtrn = []
            a = struct.pack('d', a)
            b = struct.pack('d', b)
            for ba, bb in zip(a, b):
                rtrn.append(ba ^ bb)

            return int(struct.unpack('d', bytes(rtrn))[0])  

        def running_random_value():
            start_time = time()
            i = 0
            wait_for_new_random = True
            running = 1
            full_value = 0
            while running:
                i += 1
                event = pygame.event.poll()

                if wait_for_new_random == True:
                    random.seed()
                    modulo_number = random.randrange(10,20,1)
                    wait_for_new_random = False

                if i % modulo_number == 0:
                    try:
                        full_value = float_xor(float(mouse_pos), float(full_value))
                        wait_for_new_random = True
                    except Exception as e:
                        pass

                if event.type == pygame.QUIT:
                    running = 0
                elif event.type == pygame.MOUSEMOTION:

                    mouse_pos = int("%d%d" % event.pos)
                    full_value = full_value + mouse_pos
                    #print(full_value)
                    
                screen.fill((0, 0, 0))
                pygame.display.flip()

                if time()-start_time >= movement_time:
                    return full_value

        if key_length == 256:
            phase_numbers = 32
        elif key_length == 192:
            phase_numbers = 24
        elif key_length == 128:
            phase_numbers = 16
        else:
            print("Key-Length not supported!")
            exit()


        final_key = ""

        for z in range(0, phase_numbers,1):
            print(f"---------------Round {z+1}:----------------")
            result = running_random_value()
            result = str(hex(result))[2:4]
            if result == "0":
                while True:
                    result = running_random_value()
                    result = str(hex(result))[2:4]
                    if result != "0":
                        break

            print(f"Key-part: {result}")
            final_key = final_key + str(result)

        print(f"----------------------\nFINAL-{key_length}-bit KEY: {final_key}\n----------------------")
        return final_key