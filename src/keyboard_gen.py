import struct
import keyboard
import time


class keyboard_generator():
    def random_keyboard_value(type_time, key_length):
        if key_length == 256:
            phase_numbers = 8
        elif key_length == 192:
            phase_numbers = 6
        elif key_length == 128:
            phase_numbers = 4
        else:
            print("Key-Length not supported!")
            exit()

        def float_xor(a, b):
            rtrn = []
            a = struct.pack('d', a)
            b = struct.pack('d', b)
            for ba, bb in zip(a, b):
                rtrn.append(ba ^ bb)

            return struct.unpack('d', bytes(rtrn))[0]

        
        final_key = ""

        for z in range(0, phase_numbers,1):
            first = True
            values = []
            start_time = time.time()
            print(f"---------------Round {z+1}:----------------")
            while True:
                if type_time < time.time()-start_time:
                    try:
                        result = values[0]
                    except IndexError:
                        print("Eingabe von Daten nötig!")
                        exit()

                    for i in range(1, len(values)-1,1):
                        result = float_xor(values[i], result)

                    while int(result) == 0:
                        result = result*10
                    result = int(result*10000000000000000)
                    result = str(hex(result))[2:10]
                    break

                if keyboard.read_key() != " " and first == True:
                    begin_time = time.time()
                    first = False

                elif keyboard.read_key() != " " and first == False:
                    end_time = time.time()
                    diff = end_time-begin_time
                    values.append(diff)
                    first = True
            print(f"Key-part: {result}")
            final_key = final_key + str(result)
        
        print(f"----------------------\nFINAL-{key_length}-bit KEY: {final_key}\n----------------------")
        return final_key
