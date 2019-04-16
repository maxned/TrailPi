
import time
import requests
import json

config = json.load(open("trailpi_config.json"))

def check_in():
    data = { "site" : config["site_number"] }
    headers = { "Content-Type" : "application/json" }
    response = requests.post(config["check_in_url"], data=json.dumps(data), headers=headers)

    if config["debug"]:
        print(response.status_code)
        print(response.content)

if __name__== "__main__":

    while True:
        check_in()

        # Check in every so often
        time.sleep(config["check_in_interval_sec"])
