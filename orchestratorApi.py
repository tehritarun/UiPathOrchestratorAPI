import requests
import os
import json
from dotenv import load_dotenv

# TODO: Test
# load client secret and id from .env
load_env()
clientID = os.getenv('CLIENT_ID')
clientSecret = os.getenv('CLIENT_SECRET')

KEY_FILE = "key.pem"
ORCHESTRATOR_URL = "https://cloud.uipath.com/tehri/default/orchestrator_"
AUTHENTICATION_URL = "https://account.uipath.com/oauth/token"


def read_key():
    key = ""
    if not os.path.exists(KEY_FILE):
        authenticate()
    with open(KEY_FILE, "r") as f:
        key = f.readline()
    return key


def authenticate():
    # TODO: test correct parameter as per actual authentication request
    headers = {"accept": "application/json","X-UIPATH-TenantName":"default"}
    payload={'grant_type':'refresh_token','client_id': clientID, 'refresh_token': clientSecret}
    response = requests.post(AUTHENTICATION_URL, headers=headers,data=payload)
    if response.status_code == 200:
        jsonresponse = json.loads(response.text)
        key = jsonresponse['access_token']
        with open(KEY_FILE, 'w') as f:
            f.write(key)
    else:
        response.raise_for_status()


def add_transaction(payload):
    # TODO: test correct parameter as per actual authentication request
    key = read_key()
    url=f'{ORCHESTRATOR_URL}/odata/Queues/UiPathDataSvc.AddQueueItem'
    headers = {"accept": "application/json", "authorization": f"Bearer {key}","X-UIPATH-OrganizationUnitId":"810777"}
    response = requests.post(ORCHESTRATOR_URL, headers=headers, data=payload)
    print(response)
    if response.status_code == 401:
        authenticate()
        key = read_key()
        response = requests.post(
            ORCHESTRATOR_URL, headers=headers, data=payload)
    return response.status_code
