import logging
import time
import pickle

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger('activity')

def write_file(activity):
    """Serializes the passed activity object and writes to file for reducdancy

    Arguments:
        activity - the dictionary containing site activity log
    """

    pickle_out = open("site_activity.pickle","wb")
    pickle.dump(activity, pickle_out)
    pickle_out.close()
    logger.debug('Activity log updated')

    return

def check_in(site):
    """Checks in the passed site, updating the last seen time in the activity log.

    Arguments:
        site - the site that is checking in
    """
    logger.info('Checking in site {} at {}'.format(site, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    site_activity[site] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    write_file(site_activity)

    # DEBUG outputs the values of the site_activity dictionary
    for key, value in site_activity.items():
        print(key, value)

    return

try:
    pickle_in = open("site_activity.pickle","rb")
    site_activity = pickle.load(pickle_in)
    logger.debug('Activity log existed, imported')
except FileNotFoundError:
        logger.debug('Activity log didn\'t exist, creating')
        # just initialize each site with current time
        site_activity = {}
        for site in range(1, 41):
            site_activity[str(site)] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        write_file(site_activity)

if __name__ == '__main__':
    logger.info('Testing activity.py')
