
import time
import requests
import json

def check_in():
    url = "http://flask-server.wqwtbemyjw.us-west-2.elasticbeanstalk.com/TrailPiServer/api/check_in"
    data = { "site" : 14 }
    headers = { "Content-Type" : "application/json" }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.status_code)
    print(response.content)

if __name__== "__main__":

    while True:
        check_in()

        # Check in every 30 min
        time.sleep(30 * 60)
