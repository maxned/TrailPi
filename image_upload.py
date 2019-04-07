
from datetime import datetime
import os
import time
import requests
import json

def upload_image(image_name):
    image_path = "images/{}".format(image_name) # Add the directory

    url = "http://flask-server.wqwtbemyjw.us-west-2.elasticbeanstalk.com/TrailPiServer/api/image_transfer"
    data = { "site" : 14 }

    files = [
        ("file", (image_name, open(image_path, 'rb'), "application/octet")),
        ("data", ("data", json.dumps(data), "application/json")),
    ]

    response = requests.post(url, files=files)
    print(response.status_code)
    print(response.content)

    return response

# An image is valid if the date in the filename is greater than 3 seconds old
# to make sure it has been saved to disk completely
# Return a bool whether an image is valid
def valid_image(image_name):
    image_name = image_name[:-4] # Strip the .jpg at the end of the filename
    image_time = datetime.strptime(image_name, "%m:%d:%y-%H:%M:%S:%f") # Same format as trailpi.py
    now = datetime.now()

    delta = now - image_time
    if delta.seconds >= 3:
        return True
    else:
        return False

# Return a list of image names that should be uploaded right now
def uploadable_images():
    images = os.listdir("images")
    valid_images = [image for image in images if valid_image(image)]
    return valid_images

if __name__== "__main__":

    while True:
        for image in uploadable_images():
            response = upload_image(image)

            # Delete image if successfully uploaded
            if response.status_code == 200:
                os.remove("images/{}".format(image))

        # Check every 5 seconds
        time.sleep(5)
