
import smbus
import time

bus = smbus.SMBus(1)

while True:
    bus.write_byte(0x18, 0x1)
    print("on")
    time.sleep(1)
    bus.write_byte(0x18, 0x0)
    print("off")
    time.sleep(1)
