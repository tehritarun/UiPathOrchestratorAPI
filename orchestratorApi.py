import requests
import os
import json
from dotenv import load_dotenv

# load client secret and id from .env
load_dotenv()
clientID = os.getenv("CLIENT_ID")
clientSecret = os.getenv("USER_KEY")
tanent = os.getenv("TANENT")
instanceName = os.getenv("INSTANCE_NAME")

KEY_FILE = "key.pem"
ORCHESTRATOR_URL = f"https://cloud.uipath.com/{instanceName}/{tanent}/orchestrator_"
AUTHENTICATION_URL = "https://account.uipath.com/oauth/token"


def read_key():
    key = ""
    if not os.path.exists(KEY_FILE):
        authenticate()
    with open(KEY_FILE, "r") as f:
        key = f.readline()
    return key


def authenticate():
    headers = {"accept": "application/json",
               "X-UIPATH-TenantName": f"{tanent}"}
    payload = {
        "grant_type": "refresh_token",
        "client_id": clientID,
        "refresh_token": clientSecret,
    }
    print(payload)
    response = requests.post(AUTHENTICATION_URL, headers=headers, data=payload)
    if response.status_code == 200:
        jsonresponse = json.loads(response.text)
        key = jsonresponse["access_token"]
        with open(KEY_FILE, "w") as f:
            f.write(key)
    else:
        print(response.reason)
        response.raise_for_status()


def add_transaction(payload, folderId):
    key = read_key()
    url = f"{ORCHESTRATOR_URL}/odata/Queues/UiPathODataSvc.AddQueueItem"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
        "X-UIPATH-OrganizationUnitId": folderId,
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 401:
        authenticate()
        key = read_key()
        response = requests.post(
            url, headers=headers, data=payload)
    elif response.status_code != 201:
        print(response.reason)
        print(response.content)
        response.raise_for_status()
    return response.status_code


def get_folders():
    key = read_key()
    url = f"{ORCHESTRATOR_URL}/api/Folders/GetAllForCurrentUser"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {key}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    jsonresponse = json.loads(response.text)
    return jsonresponse


# if __name__ == "__main__":
#     authenticate()
#     sampledata = {'itemData': {'SpecificContent': {"field1": "Value1", "filed2": 'Value2'},
#                                "Priority": "Normal", "Name": "TestAPIQueue", "Reference": "test"}}
#     add_transaction(json.dumps(sampledata))
