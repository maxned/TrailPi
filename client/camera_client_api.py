from sys import version_info
assert (version_info > (3, 6)), "Python 3.7 or later is required."
import logging
import os
import requests
import json

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger('CameraClientAPI')

def get_site_num():
    """Returns the site identification number for the camera.

    Arguments:
        None
    """

    # TODO implement the actual site idenfification
    return '14'

def check_in():
    """Sends a heartbeat pulse to the server so the site shows as active.

    Arguments:
        None

    Returns the response from the server.
    """
    url = "http://127.0.0.1:5000/TrailPiServer/api/check_in"

    headers = {'Content-Type': 'application/json'}

    data = {"site": get_site_num()}

    logger.info('Sending post: url = {}, data = {}, headers = {}'.format(url, data, headers))
    response = requests.post(url, data=json.dumps(data), headers=headers)
    logger.info('Response: {}'.format(response.content))

    return response

def send_image(file_path):
    """Transfers an image to the server.

    Arguments:
        file_path - path to the image to transfer

    Returns the response from the server.
    """

    url = "http://127.0.0.1:5000/TrailPiServer/api/image_transfer"

    site = {'site': get_site_num()}

    files = {
        'data': json.dumps(site),
        'file': (os.path.basename(file_path), open(file_path, 'rb'), 'application/octet-stream')
    }

    logger.info('files: {}'.format(files))
    response = requests.post(url, files=files)
    logger.info('Response: {}'.format(response.content))

    return response

def run_testing():
    print('Modes:\n'
          '\t0: check_in\n'
          '\t1: send_image\n'
          '\t123: quit')

    while True:
        choice = input('Choose a mode: ')
        try:
            val = int(choice)
            if val == 0:
                check_in()
                break
            elif val == 1:
                test_image = 'test_image.png'
                send_image(test_image)
                break
            elif val == 123:
                logger.info('Done testing')
                break
            else:
                logger.warning('Invalid choice')
        except ValueError:
            print('Input wasn\'t a number!')


if __name__ == "__main__":
    logger.info('Testing camera_client_api.py')
    run_testing()
