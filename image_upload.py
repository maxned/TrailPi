
from datetime import datetime
import os
import time
import requests
import json

config = json.load(open("trailpi_config.json"))

def upload_image(image_name):
    image_path = "{}/{}".format(config["image_folder"], image_name) # Add the directory

    site_data = { "site" : config["site_number"] }
    image_data = None

    try:
        image_data = open(image_path, 'rb')
    except:
        if config["debug"]:
            print("Image cannot be opened: {}".format(image_path))

        return requests.models.Response()

    files = [
        ("file", (image_name, image_data, "application/octet")),
        ("data", ("data", json.dumps(site_data), "application/json")),
    ]

    try:
        response = requests.post(config["image_upload_url"], files=files)
    except:
        if config["debug"]:
            print("POST request failed")

        return requests.models.Response()

    if config["debug"]:
        print(response.status_code)
        print(response.content)

    return response

# An image is valid if the date in the filename is greater than a few seconds old
# to make sure it has been saved to disk completely
# Return a bool whether an image is valid
def valid_image(image_name):
    image_name = image_name[:-4] # Strip the .jpg at the end of the filename
    image_time = datetime.strptime(image_name, config["image_timestamp_format"]) # Same format as trailpi.py
    now = datetime.now()

    delta = now - image_time
    if delta.seconds >= config["image_upload_valid_image_delta"]:
        return True
    else:
        return False

# Return a list of image names that should be uploaded right now
def uploadable_images():
    images = os.listdir(config["image_folder"])
    valid_images = [image for image in images if valid_image(image)]
    return valid_images

if __name__== "__main__":

    while True:
        for image in uploadable_images():
            response = upload_image(image)

            # Delete image if successfully uploaded
            if response.status_code == 200:
                os.remove("{}/{}".format(config["image_folder"], image))

        # Check every 5 seconds
        time.sleep(config["image_upload_check_interval_sec"])
