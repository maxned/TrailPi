
import time
import requests
import json
import helpers
import os

log = helpers.setup_logger(os.path.basename(__file__))
log.info("Starting execution")

if os.path.exists("/boot/trailpi_config.json"):
    config_file = "/boot/trailpi_config.json"
else:
    config_file = "trailpi_config.json"

config = json.load(open(config_file))

site_data = { "site" : config["site_number"] }
headers = { "Content-Type" : "application/json" }

while True:
    try:
        response = requests.post(config["check_in_url"], data=json.dumps(site_data), headers=headers)
    except:
        log.error("POST request failed")
    else:
        log.info(response.status_code)
        log.info(response.content)

    # Check in every so often
    time.sleep(config["check_in_interval_sec"])
