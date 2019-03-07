import time
import pickle
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Living')

try:
    pickle_in = open("site_activity.pickle","rb")
    site_activity = pickle.load(pickle_in)
    logger.debug('Activity log exists, importing')

except FileNotFoundError:
        logger.debug('Activity log didn\'t exist, creating')
        # just initialize each site with current time
        site_activity = {}
        for site in range(1, 41):
            site_activity[str(site)] = time.localtime(time.time())

        # save to file for future use
        pickle_out = open("site_activity.pickle","wb")
        pickle.dump(site_activity, pickle_out)
        pickle_out.close()

def check_in(site):
    """Checks the passed site in, updating the last seen time in the activity log.

    Arguments:
        site - the site that is checking in
    """
    logger.info('Checking in site {} at {}'.format(site, time.localtime(time.time())))
    site_activity[site] = time.localtime(time.time())

    # serialize site_activity and log it to file for redundancy
    pickle_out = open("site_activity.pickle","wb")
    pickle.dump(site_activity, pickle_out)
    pickle_out.close()
    logger.debug('Activity log updated')

    for key, value in site_activity.items():
        print(key, value)

if __name__ == '__main__':
    logger.info('Testing Living.py')
