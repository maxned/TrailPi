
import time
import requests
import json

config = json.load(open("trailpi_config.json"))

def check_in():
    site_data = { "site" : config["site_number"] }
    headers = { "Content-Type" : "application/json" }

    try:
        response = requests.post(config["check_in_url"], data=json.dumps(site_data), headers=headers)
    except:
        if config["debug"]:
            print("POST request failed")
    else:
        if config["debug"]:
            print(response.status_code)
            print(response.content)

if __name__== "__main__":

    while True:
        check_in()

        # Check in every so often
        time.sleep(config["check_in_interval_sec"])
