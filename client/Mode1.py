import logging
import requests

def get_site_num():
    """Returns the identification number for the camera's site.
    """
    # TODO implement the actual site idenfification

    return '14'

def execute(image):
    url = "http://127.0.0.1:5000/TrailPiServer/api/image_transfer"

    headers = {'Content-Type': 'image/png'}

    data = {'file': image}

    response = requests.post(url, data = data, headers = headers)
    logger.info('Response: {}'.format(response))

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger('Mode1')

if __name__ == '__main__':
    logger.info('Testing Mode1.py')
