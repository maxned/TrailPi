
from picamera import PiCamera
from gpiozero import MotionSensor, DigitalOutputDevice
from datetime import datetime
import helpers
import json
import smbus
import time
import signal
import io
import piexif
import os

# Global variables set in main
log = None
config = None
pir_output = None
pir_input = None
relay = None
take_picture = False

def take_picture(signum, frame):
    log.debug("Signal take picture")

    global take_picture
    take_picture = True

def enable_capture(signum, frame):
    log.info("Signal capture enabled")

    global capture_enabled
    capture_enabled = True

def disable_capture(signum, frame):
    log.info("Signal capture disabled")

    global capture_enabled
    capture_enabled = False

def motion_detected():
    log.info("motion detected: {}".format(pir_input.value))

    # Mirror the output of the PIR sensor for the other Pi
    pir_output.value = pir_input.value

    if pir_input.value and capture_enabled:
        global take_picture
        take_picture = True

def switch_to_other_camera():
    log.info("Switch to other camera")

    pid = helpers.get_pid("trailpi.py")
    if pid == 0: # trailpi isn't running for some reason
        log.warning("trailpi.py PID not found")
        return

    # Signal to trailpi.py that the night camera should be enabled and self
    # should be disabled
    os.kill(pid, signal.SIGUSR1)

def set_ir_led_state(state):
    global relay
    if state == True:
        relay.write_byte(0x18, 0x1)
    else:
        relay.write_byte(0x18, 0x0)

def save_picture(image, timestamp):
    if image:
        try:
            # Make sure directory exists
            if not "images" in os.listdir():
                os.mkdir("images")

            with open('{}/{}.jpg'.format(config["image_folder"], timestamp), 'wb') as file:
                file.write(image)

                # Make sure file is saved to disk so it can be uploaded
                file.flush()
                os.fsync(file.fileno())

                log.info("Saved image: {}.jpg".format(timestamp))
        except:
            log.error("Failed saving image to disk: {}".format(timestamp))

def begin_image_capture():
    camera = PiCamera(resolution=tuple(config["resolution"]))
    # Encode the site number into the exif field of the image just in case
    camera.exif_tags["EXIF.SubjectDistanceRange"] = str(config["site_number"])
    time.sleep(2) # Give camera time to wake up

    # Goal is keep capturing images and saving images to a buffer
    # When told to take_picture, save the buffered images to disk
    # Then save the current image to disk and the same number of buffered images after

    # Images to save before and after take_picture event
    buffer_size = int(config["capture_chunk_size"] / 2)
    image_buffer = helpers.RingBuffer(buffer_size)
    left_to_save = 0

    stream = io.BytesIO()
    # Quality is not in percentage, it is logarithmic
    # Do not save the thumbnail to keep the file size smaller
    for capture in camera.capture_continuous(stream, format='jpeg',
                                            quality=config["quality"], thumbnail=None):

        log.info("Image captured")
        log.info("Analog_gain: " + str(float(camera.analog_gain)))
        log.info("Digital_gain: " + str(float(camera.digital_gain)))

        # Timestamp the image
        timestamp = datetime.now().strftime(config["image_timestamp_format"])

        # Event happened so save buffered images and start saving future images
        global take_picture
        if take_picture == True:
            take_picture = False

            # Save buffered images to disk
            for image, im_timestamp in image_buffer.get():
                save_picture(image, im_timestamp)

            # Clear buffered images
            image_buffer.clear()

            # Number of images to save past the take_picture event
            # including the image right after the event
            left_to_save = buffer_size + 1

        if left_to_save > 0:
            # These are the images saved to disk after the take_picture event
            save_picture(stream.getvalue(), timestamp)
            left_to_save -= 1
        else:
            # Save images into buffer if not saving them to disk
            # Save as tuple together with the timestamp
            image_buffer.append((stream.getvalue(), timestamp))

        # Reset the stream to capture a new image
        stream.seek(0)
        stream.truncate()

        # Switch to the other camera based on the specified threshold
        if config["camera_type"] == "day" and capture_enabled and \
                camera.analog_gain > config["day_to_night_threshold"]:
            switch_to_other_camera()
        elif config["camera_type"] == "night" and capture_enabled and \
                camera.analog_gain < config["night_to_day_threshold"]:
            switch_to_other_camera()

        # Sleep between images (needed to allow auto exposure to work)
        # Values of at least 0.1 will allow camera to expose within 10 seconds
        # Higher values will allow for faster exposure
        time.sleep(config["inter_capture_delay"])

        # If capture is disabled, stop taking pictures and suspend the whole script
        while not capture_enabled:
            signal.pause()

if __name__== "__main__":
    log = helpers.setup_logger(os.path.basename(__file__))
    log.info("Starting execution")

    config = json.load(open("trailpi_config.json"))

    # Default value for whether image capture should be enabled on start
    # depending on camera_type (day or night)
    if config["camera_type"] == "day":
        capture_enabled = True
    else:
        capture_enabled = False

    # PIR output that mirrors PIR input for use by the other Pi
    pir_output = DigitalOutputDevice(config["pir_output_pin"])

    # PIR connected to GPIO pin
    pir_input = MotionSensor(config["pir_input_pin"])
    pir_input.when_motion = motion_detected
    pir_input.when_no_motion = motion_detected

    # Setup relay i2c communication on i2c bus 1 (default)
    relay = smbus.SMBus(1)

    # Manually trigger a take_picture event (only for debug)
    if config["debug"]:
        signal.signal(signal.SIGINT, take_picture)

    # Sign up for signals to control whether capture should be enabled or disabled
    signal.signal(signal.SIGUSR1, enable_capture)
    signal.signal(signal.SIGUSR2, disable_capture)

    # Keep taking pictures but save them only when needed
    begin_image_capture()
