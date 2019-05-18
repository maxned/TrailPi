
# This script is in charge of uploading images to the server.

# Basic method of operation:
# - Check for images in the image folder every so often.
# - If an image exists, upload it to the server.
# - If successfully uploaded, delete the image.

from datetime import datetime
import os
import time
import requests
import json
import helpers

# Global variables set in main
log = None
config = None

def upload_image(image_name):
    image_path = "{}/{}".format(config["image_folder"], image_name) # Add the directory

    site_data = { "site" : config["site_number"] }
    image_data = None

    try:
        # Make sure directory exists
        if not config["image_folder"] in os.listdir():
            os.mkdir(config["image_folder"])

        image_data = open(image_path, 'rb')
    except:
        log.error("Image cannot be opened: {}".format(image_path))
        return requests.models.Response()

    files = [
        ("file", (image_name, image_data, "application/octet")),
        ("data", ("data", json.dumps(site_data), "application/json")),
    ]

    try:
        response = requests.post(config["image_upload_url"], files=files)
    except:
        log.error("POST request failed for image: {}".format(image_name))
        return requests.models.Response()

    log.info("Uploaded image: {}".format(image_name))
    log.info(response.status_code)
    log.info(response.content)

    return response

# An image is valid if the date in the filename is greater than a few seconds old
# to make sure it has been saved to disk completely
# Return a bool whether an image is valid
def valid_image(image_name):
    image_name = image_name[:-4] # Strip the .jpg from the end of the filename
    image_time = datetime.strptime(image_name, config["image_timestamp_format"])
    now = datetime.now()

    delta = now - image_time
    if delta.seconds >= config["image_upload_valid_image_delta"]:
        return True
    else:
        return False

# Return a list of image names that should be uploaded right now
def uploadable_images():
    # Make sure directory exists before searching it
    if not config["image_folder"] in os.listdir():
        os.mkdir(config["image_folder"])

    images = os.listdir(config["image_folder"])
    valid_images = [image for image in images if valid_image(image)]
    return valid_images

if __name__== "__main__":
    log = helpers.setup_logger(os.path.basename(__file__))
    log.info("Starting execution")

    if os.path.exists("/boot/trailpi_config.json"):
        config_file = "/boot/trailpi_config.json"
    else:
        config_file = "trailpi_config.json"

    config = json.load(open(config_file))

    while True:
        for image_name in uploadable_images():
            response = upload_image(image_name)

            # Delete image if successfully uploaded
            if response.status_code == 200:
                try:
                    os.remove("{}/{}".format(config["image_folder"], image_name))
                    log.info("Removed image: {}".format(image_name))
                except:
                    log.error("Could not remove image: {}".format(image_name))

        # Check every so often
        time.sleep(config["image_upload_check_interval_sec"])
