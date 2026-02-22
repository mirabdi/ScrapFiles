import json
import requests
import ast 
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.common import write_to_json, read_json, calculate_time, clean_phone
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL


def revive_client(id):
    params = {
        "path": f"/data/57c09c3b3ce7d59d048b46c9/clients/{id}",
        "api": "v3", 
        "timezone": "32400",
    }
    response = requests.get(
        url=COMMON_URL,
        headers=COMMON_HEADERS,
        params=params,
    )
    print(f"Reviving client ID: {id}")
    if response.status_code == 200 and response.json().get('status'):
        name = response.json().get('data')['name']
        payload = {
            "name": name,
            "deleted": False
        }
        print(f"Reviving client ID: {id} with name: {name}")
        revive_response = requests.put(
            url=COMMON_URL,
            headers=COMMON_HEADERS,
            params=params,
            json=payload
        )
        if revive_response.status_code == 200 and revive_response.json().get('status'):
            return True
    return False

def revive_clients():
    # read clients_for_revival.txt file and makes clients list
    with open("clients_for_revival.txt", "r") as file:
        text = file.read()

    clients = ast.literal_eval(text)
    print(f"Total clients to revive: {len(clients)}")
    for c_id in clients:
        cnt = 0
        while True:
            try:
                success = revive_client(c_id)
                if not success:
                    print(f"Couldn't revive client ID: {c_id}")
                else:
                    break
            except Exception as e:
                print(f"Error reviving client ID {c_id}: {e}")
                cnt += 1

if __name__ == "__main__":
    revive_clients()