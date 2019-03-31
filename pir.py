
from gpiozero import MotionSensor

x = 0

def got_motion():
    global x
    print("motion" + str(x))
    x += 1

pir = MotionSensor(18)
pir.when_motion = got_motion
print("started")

while True:
    continue
