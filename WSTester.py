import serial
import time
from time import ctime

HeatRelay_W1on = b'@00 ON 1\r'
CoolRelay_Y1on = b'@00 ON 2\r'
FanL_Gon = b'@00 ON 3\r'
FanM_W2on = b'@00 ON 4\r'
FanH_Y2on = b'@00 ON 5\r'

HeatRelay_W1off = b'@00 OF 1\r'
CoolRelay_Y1off = b'@00 OF 2\r'
FanL_Goff = b'@00 OF 3\r'
FanM_W2off = b'@00 OF 4\r'
FanH_Y2off = b'@00 OF 5\r'
all_off = b'@00 OF 0\r'

acON = b'\x01\x06\x00\x00\x00\x01H\n'
acOFF = b'\x01\x06\x00\x00\x00\x00\x89\xca'
heat = b'\x01\x06\x00\x01\x00\x01\x19\xca'
heatSP = b'\x01\x06\x00\x04\x00\x1c\xc9\xc2'
cool = b'\x01\x06\x00\x01\x00\x04\xd9\xc9'
coolSP = b'\x01\x06\x00\x04\x00\x12H\x06'

fan = b'\x01\x06\x00\x01\x00\x03\x98\x0b'

fanLOW = b'\x01\x06\x00\x02\x00\x01\xe9\xca'
fanMED = b'\x01\x06\x00\x02\x00\x02\xa9\xcb'
fanHIGH = b'\x01\x06\x00\x02\x00\x03h\x0b'


def ws_test():
    with serial.Serial('COM4', 9600, timeout=5000, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE) as kta:
        print("KTA Port Open: COM4")
        kta.write(all_off)

        with serial.Serial('COM8', 9600, timeout=7000, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE) as ser:
            print("DUT Port Open: COM8")

            c = '>'
            while c != 'Q':
                print("Test Start Time:", ctime())
                print("\nPower cycle the DUT ")

                ser.write(0x1f)
                s = ser.read(8)
                time.sleep(0.2)
                ser.write(s)
                if s == acOFF:
                    print("AC OFF: PASS ")  # print("Time:",ctime())
                else:
                    print("AC OFF: FAIL")
                    print("Time:", ctime())
                    input()
                    break

                kta.write(HeatRelay_W1on)
                print("\nTESTING HEAT MODE")

                ser.write(0x1f)
                s = ser.read(8)
                time.sleep(0.2)
                ser.write(s)

                if s == acON:
                    print("AC ON:PASS")  # print("Time:",ctime())
                else:
                    print("AC ON: FAIL")
                    print("Time:", ctime())
                    input()
                    break

                ser.write(0x1f)
                s = ser.read(8)
                time.sleep(0.2)
                ser.write(s)

                if s == heat:
                    print("AC MODE PASS: HEAT ")  # print("Time:",ctime())
                else:
                    print("AC MODE: FAIL")
                    print("Time:", ctime())
                    input()
                    break

                ser.write(0x1f)
                s = ser.read(8)
                time.sleep(0.2)
                ser.write(s)

                if s == heatSP:
                    print("HEAT SET POINT PASS: 28 DEG C ")  # print("Time:",ctime())
                else:
                    print("HEAT SET POINT: FAIL")
                    print("Time:", ctime())
                    input()
                    break

                kta.write(HeatRelay_W1off)
                time.sleep(0.1)
                kta.write(CoolRelay_Y1on)
                time.sleep(0.1)
                kta.write(FanL_Gon)
                print("\nTESTING COOL MODE ")

                ser.write(0x1f)
                s = ser.read(8)
                time.sleep(0.2)
                ser.write(s)

                if s == cool:
                    print("AC MODE PASS: COOL ")  # print("Time:",ctime())
                else:
                    print("AC MODE: FAIL")
                    print("Time:", ctime())
                    input()
                    break

                ser.write(0x1f)
                s = ser.read(8)
                time.sleep(0.2)
                ser.write(s)

                if s == coolSP:
                    print("COOL SET POINT PASS: 18 DEG C")  # print("Time:",ctime())
                else:
                    print("COOL SET POINT: FAIL \n")
                    print("Time:", ctime())
                    input()
                    break

                print("\nTESTING FAN SPEED LOW")

                ser.write(0x1f)
                s = ser.read(8)
                time.sleep(0.2)
                ser.write(s)

                if s == fanLOW:
                    print("FAN SPEED SET TO LOW: PASS")
                else:
                    print("FAN SPEED SET: FAIL")
                    print("Time:", ctime())
                    input()
                    break

                kta.write(FanL_Goff)
                time.sleep(0.1)
                kta.write(FanM_W2on)
                print("\nTESTING FAN SPEED MED")

                ser.write(0x1f)
                s = ser.read(8)
                time.sleep(0.2)
                ser.write(s)

                if s == fanMED:
                    print("FAN SPEED SET TO MED: PASS")
                else:
                    print("FAN SPEED SET: FAIL")
                    print("Time:", ctime())
                    input()
                    break

                kta.write(FanM_W2off)
                time.sleep(0.1)
                kta.write(FanH_Y2on)
                print("\nTESTING FAN SPEED HIGH")

                ser.write(0x1f)
                s = ser.read(8)
                time.sleep(0.2)
                ser.write(s)

                if s == fanHIGH:
                    print("FAN SPEED SET TO HIGH: PASS")
                else:
                    print("FAN SPEED SET: FAIL")
                    print("Time:", ctime())
                    input()
                    break

                print("\nDUT PASSED ALL TEST, FLASH APPLICATION FIRMWARE ")
                c = 'Q'


def ws_testerapp():
    with serial.Serial('COM4', 9600, timeout=5000, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE) as kta:
        print("KTA Port Open: COM4")

        with serial.Serial('COM8', 9600, timeout=7000, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE) as ser:
            print("Zen Whitesands Port Open: COM8")

            ser.write(0x1f)
            s = ser.read(8)
            time.sleep(0.2)
            ser.write(s)
            if s == acON:
                print("AC ON: PASS ")
                print("Time:", ctime())
                print("\nDUT  - APPLICATION FIRMWARE TEST PASSED")
                return 0
            else:
                print("AC OFF: FAIL")
                print("Time:", ctime())
                return 1



