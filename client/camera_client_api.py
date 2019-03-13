from sys import version_info
assert (version_info > (3, 7)), "Python 3.7 or later is required."
import logging
import os
import requests

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

    headers = {'Content-Type': 'text/plain'}

    data = {'site': ('', get_site_num())}

    logger.info('Sending post: url = {}, data = {}, headers = {}'.format(url, data, headers))
    response = requests.post(url, data = data, headers = headers)
    logger.info('Response: {}'.format(response))

    return response

def send_image(file_path):
    """Transfers an image to the server.

    Arguments:
        file_path - path to the image to transfer

    Returns the response from the server.
    """

    url = "http://127.0.0.1:5000/TrailPiServer/api/image_transfer"

    headers = {'Content-Type': 'image/png'}

    data = {'file': (os.path.basename(file_path), open(file_path, 'rb')),
            'site': ('', get_site_num())}

    logger.info('Sending post: url = {}, data = {}, headers = {}'.format(url, data, headers))
    response = requests.post(url, data = data, headers = headers)
    logger.info('Response: {}'.format(response))

    return response
