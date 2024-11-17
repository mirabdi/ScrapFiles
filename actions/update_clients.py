import json
import openpyxl
import requests
from config import COMMON_HEADERS, COMMON_URL, BASE_URL
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

# COMPANY_ID = '66d70e3ca35f222ea66fa1c6' # test 
COMPANY_ID = '57c09c3b3ce7d59d048b46c9' # original

def update_client(cloudshop_id, name, bonus_balance, bonus_spent):
    params = {
        "path": f"/data/{COMPANY_ID}/clients/{cloudshop_id}",
        "api": "v3",
        "timezone": "21600",
    }
    headers = COMMON_HEADERS
    data_payload = {
        "name": name,
        "discount": None,
        "loyalty_type": "bonus",
        "bonus_balance": bonus_balance,
        "bonus_spent": bonus_spent,
        "enable_savings": False,
    }
    response = requests.put(COMMON_URL, headers=headers, params=params, json=data_payload)
    
    if response.status_code == 200 and response.json().get('status'):
        print(f"Successfully updated client {name} ({cloudshop_id})")
    else:
        print(f"Failed to update client {name}. Status code: {response.status_code}")
        print("Response:", response.text)


def update_clients_from_preserve():
    # Read preserve.txt for cloudshop_ids
    with open("preserve.txt", "r", encoding="utf-8") as preserve_file:
        cloudshop_ids = [line.strip() for line in preserve_file if line.strip()]

    # Load merged_clients.json
    with open("merged_clients.json", "r", encoding="utf-8") as clients_file:
        merged_clients = json.load(clients_file)

    # Create a dictionary for fast lookup of clients by cloudshop_id
    client_dict = {client['cloudshop_id']: client for client in merged_clients}

    # Update clients from preserve.txt
    for cloudshop_id in cloudshop_ids:
        if cloudshop_id in client_dict:
            client = client_dict[cloudshop_id]
            name = client.get('name', 'Unknown')
            bonus_balance = client.get('bonus_balance', 0)
            bonus_spent = client.get('bonus_spent', 0)
            update_client(cloudshop_id, name, bonus_balance, bonus_spent)
        else:
            print(f"Client with cloudshop_id {cloudshop_id} not found in merged_clients.json")

if __name__ == "__main__":
    update_clients_from_preserve()
