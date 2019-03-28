# Some code taken from https://github.com/erogol/RaspiSecurity

from picamera.array import PiRGBArray
from picamera import PiCamera
import json
import time
import cv2

config = json.load(open("config.json"))

camera = PiCamera()
camera.resolution = tuple(config["full_res"])
#camera.framerate = config["fps"]
raw_capture = PiRGBArray(camera, size=camera.resolution)

# Sleep to allow camera to wake up
time.sleep(2)

avg = None
motionCounter = 0
object_detected = False

# Continually capture frames from the camera
while True:
    object_detected = False

    camera.capture(raw_capture, format="bgr", use_video_port=True)
    print("image captured")

    low_res_frame = cv2.resize(raw_capture.array, tuple(config["low_res"]))

    # Convert image to grayscale and blur it for comparison against running average
    gray = cv2.cvtColor(low_res_frame, cv2.COLOR_BGR2GRAY)
    blurred_gray = cv2.GaussianBlur(gray, tuple(config['blur_size']), 0)

    # If no average frame, create it
    if avg is None:
        avg = blurred_gray.copy().astype("float")
        raw_capture.truncate(0)
        continue

    # Compute the difference between the current frame and running average
    # then update the running average with the current frame
    frame_delta = cv2.absdiff(blurred_gray, cv2.convertScaleAbs(avg))
    cv2.accumulateWeighted(blurred_gray, avg, config["running_average_update"])

    # Threshold the delta image, dilate it to fill in holes, then find the contours
    thresholded = cv2.threshold(frame_delta, config["delta_threshold"], 255, cv2.THRESH_BINARY)[1]
    thresholded = cv2.dilate(thresholded, None, iterations=2)
    _ , contours, _ = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the contour that is larger than the min_area
    for area in contours:
        # If the contour is too small, ignore it
        if cv2.contourArea(area) < config["min_area"]:
            continue

        object_detected = True

    # If object is detected, save the image
    if object_detected:
        # Save full resolution current frame
        cv2.imwrite("full_frame_{}.jpg".format(motionCounter), raw_capture.array)

        if config["debug"]:
            cv2.imwrite("frame_{}.jpg".format(motionCounter), low_res_frame)
            cv2.imwrite("frame_gray_{}.jpg".format(motionCounter), blurred_gray)
            cv2.imwrite("frame_thres_{}.jpg".format(motionCounter), thresholded)
            cv2.imwrite("frame_avg_{}.jpg".format(motionCounter), avg)
            cv2.imwrite("frame_delta_{}.jpg".format(motionCounter), frame_delta)

        print("saved image {}".format(motionCounter))
        motionCounter += 1

    # Clear the stream in preparation for the next frame
    raw_capture.truncate(0)
