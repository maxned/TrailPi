import datetime

def check_in(site):
    """Checks in the passed site, updating the last seen time in the activity log.

    Arguments:
        site - the site that is checking in
    """
    site_activity[site] = datetime.datetime.now()


# just initialize each site with current time
print('initializing site activity')
site_activity = {}
for site in range(1, 41):
    site_activity[str(site)] = datetime.datetime.now()
