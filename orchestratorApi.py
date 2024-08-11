import requests
import os
import json

# TODO
# load client secret and id from .env
clientID = ''
clientSecret = ''

KEY_FILE = "key.pem"
ORCHESTRATOR_URL = ""
AUTHENTICATION_URL = "https://cloud.uipath.com/identity_/connect/authorize"


def read_key():
    key = ""
    if not os.path.exists(KEY_FILE):
        authenticate()
    with open(KEY_FILE, "r") as f:
        key = f.readline()
    return key


def authenticate():
    # TODO: correct parameter as per actual authentication request
    headers = {"accept": "application/json",
               'clientId': clientID, 'client_secret': clientSecret}
    response = requests.post(AUTHENTICATION_URL, headers=headers)
    if response.status_code == 204:
        jsonresponse = json.loads(response.text)
        key = jsonresponse['token']
        with open(KEY_FILE, 'w') as f:
            f.write(key)
    else:
        response.raise_for_status()


def add_transaction(payload):
    # TODO: correct parameter as per actual authentication request
    key = read_key()
    headers = {"accept": "application/json", "authorization": f"Bearer {key}"}
    response = requests.post(ORCHESTRATOR_URL, headers=headers, data=payload)
    print(response)
    if response.status_code == 401:
        authenticate()
        key = read_key()
        response = requests.post(
            ORCHESTRATOR_URL, headers=headers, data=payload)
    return response.status_code
