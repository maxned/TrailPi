
# This script is in charge of switching from one Pi to the other for day/night
# camera operation.

# Basic method of operation:
# - This script listens for a signal from image_capture.py to switch cameras.
# - Once it receives the signal, it tells the other Pi that it wants to switch.
# - The other Pi has this identical script running and when its input goes HIGH,
#   it starts its own image capture and tells the signaling Pi to stop image
#   capture.
# - This method ensures that the current Pi will only stop capturing images once
#   it knows that the other Pi is now capturing images.

import os
import signal
import time
import gpiozero
import json
import helpers

# Global variables set in main
log = None
config = None
input_pin = None
output_pin = None

def start_image_capture():
    pid = helpers.get_pid("image_capture.py")
    if pid == 0: # image_capture isn't running for some reason
        log.warning("image_capture.py PID not found")
        return

    # Start self image capture
    os.kill(pid, signal.SIGUSR1)

    # Set the inverse of the input for the other Pi
    # Tell other Pi to stop image capture
    output_pin.off()

    log.info("Start image capture")

def stop_image_capture():
    pid = helpers.get_pid("image_capture.py")
    if pid == 0: # image_capture isn't running for some reason
        log.warning("image_capture.py PID not found")
        return

    # Stop self image capture
    os.kill(pid, signal.SIGUSR2)

    # Set the inverse of the input for the other Pi
    # Tell other Pi to start image capture
    output_pin.on()

    log.info("Stop image capture")

def tell_other_pi_to_turn_on(signum, frame):
    # Tell other Pi to start image capture and cycle its input to make sure it
    # catches the edge
    output_pin.off()
    time.sleep(0.5)
    output_pin.on()

if __name__== "__main__":
    log = helpers.setup_logger(os.path.basename(__file__))
    log.info("Starting execution")

    if os.path.exists("/boot/trailpi_config.json"):
        config_file = "/boot/trailpi_config.json"
    else:
        config_file = "trailpi_config.json"

    config = json.load(open(config_file))

    # For the day camera we want to prefer starting capture
    # For the night camera, prefer not capturing by default
    if config["camera_type"] == "day":
        default_output = False
        default_pullup = True
    else:
        default_output = True
        default_pullup = False

    # Setup INPUT pin from the other Pi to know when to enable capture
    input_pin = gpiozero.DigitalInputDevice(config["pi2_input_pin"], pull_up=default_pullup)
    input_pin._active_state = True # Hack to make HW value of pin match SW value
    input_pin.when_activated = start_image_capture
    input_pin.when_deactivated = stop_image_capture

    # OUTPUT pin specified to the other Pi that it should enable or disable capture
    output_pin = gpiozero.DigitalOutputDevice(config["pi2_output_pin"], initial_value=default_output)

    # Make sure to set the appropriate things on startup
    if input_pin.value == 0:
        stop_image_capture()
    else:
        start_image_capture()

    # Sign up for signal to control whether capture should be enabled or disabled
    # SIGUSR1 tells self to stop capture and enable the other camera
    signal.signal(signal.SIGUSR1, tell_other_pi_to_turn_on)

    # Wait "indefinitely" (really until any type of signal)
    # The event based functions will continue to fire but we want to not waste
    # CPU cycles when waiting
    while True:
        signal.pause()
