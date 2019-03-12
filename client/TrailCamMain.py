from sys import version_info
assert (version_info > (3, 7)), "Python 3.7 or later is required."
import logging

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger('TrailCamMain')

def run_testing():
    """Loop that lets you set the mode for testing purposes.

    Inputs:
        None
    """

    print("Welcome to client testing!\n"
          "Modes:\n"
          "   0: Check-in\n"
          "   1: New image\n"
          "   123: quits testing")

    while True:
        mode = input('Which mode do you want to connect for? ')
        try:
            mode = int(mode)
        except ValueError:
            logger.error('Input was not an int!')
            continue

        if mode == 123:
            logger.info('Quitting...')
            return

def main():
    # TODO implement logic for when to check-in and when to transfer an image

    run_testing()

if __name__ == '__main__':
    main()
