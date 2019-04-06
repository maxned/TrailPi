
from picamera import PiCamera
from gpiozero import MotionSensor
from datetime import datetime
import smbus
import time
import signal
import io

pir = None
relay = None
take_picture = False

# From the Python Cookbook
# Default list is populated with tuples of (None, None)
class RingBuffer:
    def __init__(self, size_max):
        self.max = size_max
        self.current = 0
        self.clear()

    # Append an element overwriting the oldest one
    def append(self, x):
        self.data[self.current] = x
        self.current = (self.current + 1) % self.max

    # Return elements from oldest to newest
    def get(self):
        return self.data[self.current:] + self.data[:self.current]

    def clear(self):
        self.data = [(None, None) for i in range(self.max)]

def take_picture(signum, frame):
    print("take picture")
    global take_picture
    take_picture = True

def motion_detected():
    print("motion detected")

def set_ir_led_state(state):
    global relay
    if state == True:
        relay.write_byte(0x18, 0x1)
    else:
        relay.write_byte(0x18, 0x0)

def set_pir_state(state):
    global pir
    if state == True:
        pir.when_motion = motion_detected
    else:
        pir.when_motion = None

def begin_image_capture():
    #camera = PiCamera(resolution=(3280, 2464))
    camera = PiCamera(resolution=(640, 480))
    time.sleep(2) # Give camera time to wake up

    # Goal is keep capturing images and saving images to a buffer
    # When told to take_picture, save the buffered images to disk
    # Then save the current image to disk and the same number of buffered images after

    buffer_size = 2 # Images to save before and after take_picture event
    image_buffer = RingBuffer(buffer_size)
    left_to_save = 0

    stream = io.BytesIO()
    for capture in camera.capture_continuous(stream, format='jpeg'):

        # Timestamp the image
        timestamp = datetime.now().strftime("%d:%m:%y-%H:%M:%S:%f")

        # Event happened so save buffered images and start saving future images
        global take_picture
        if take_picture == True:
            take_picture = False

            # Save buffered images to disk
            for image, im_timestamp in image_buffer.get():
                if image:
                    with open('images/{}.jpg'.format(im_timestamp), 'wb') as file:
                        file.write(image)

            # Clear buffered images
            image_buffer.clear()

            # Number of images to save past the take_picture event
            # including the image right after the event
            left_to_save = buffer_size + 1

        if left_to_save > 0:
            with open('images/{}.jpg'.format(timestamp), 'wb') as file:
                file.write(stream.getvalue())
                left_to_save -= 1
        else:
            # Save images into buffer if not saving them to disk
            # Save as tuple together with the timestamp
            image_buffer.append((stream.getvalue(), timestamp))

        stream.seek(0)
        stream.truncate()

        print("captured image")

if __name__== "__main__":
    print("starting")

    # PIR connected to GPIO pin 18
    pir = MotionSensor(18)

    # Setup relay i2c communication on i2c bus 1 (default)
    relay = smbus.SMBus(1)

    # Manually trigger a take_picture event
    signal.signal(signal.SIGINT, take_picture)

    # Keep taking pictures but save them only when needed
    begin_image_capture()
