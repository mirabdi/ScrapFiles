import json
import openpyxl
import requests
from config import COMMON_HEADERS, COMMON_URL, BASE_URL
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

# COMPANY_ID = '66d70e3ca35f222ea66fa1c6' # test 
COMPANY_ID = '57c09c3b3ce7d59d048b46c9' # original

client_data_layout = {
    "type": "person",
    "emails": [""],
    "phones": [""],
    "enable_savings": False,
    "address": {
        "actual": None,
        "legal": None
    },
    "details": [],
    "bank_details": [],
    "discount": None,
    "default": False,
    "loyalty_type": "discount",
    "bonus_balance": 0,
    "bonus_spent": 0,
    "cashback_rate": 0,
    "name": "Client 11",
    "bday": 1727132662
}



def load_client(cloudshop_id):
    params = {
        "path": f"/data/{COMPANY_ID}/clients/{cloudshop_id}",
        "api": "v3",
        "timezone": "21600",
    }
    response = requests.get(COMMON_URL, headers=COMMON_HEADERS, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to load client. Status code:", response.status_code)
        print("Response:", response.text)
        return None


def create_client():
    params = {
        "path": f"/data/{COMPANY_ID}/clients/",
        "api": "v3",
        "timezone": "21600",
    }
    headers = COMMON_HEADERS
    data_payload = {}
    response = requests.post(COMMON_URL, headers=headers, params=params, json=data_payload)
    
    if response.status_code == 200:
        print("Client created successfully:", response.json())
    else:
        print("Failed to create client. Status code:", response.status_code)
        print("Response:", response.text)


def update_client(cloudshop_id, name):
    params = {
        "path": f"/data/{COMPANY_ID}/clients/{cloudshop_id}",
        "api": "v3",
        "timezone": "21600",
    }
    headers = COMMON_HEADERS
    data_payload = {
        "name" : name,
        "discount" : None,
        "loyalty_type" : "bonus",
        "bonus_balance" : 120,
        "enable_savings": False,
    }
    response = requests.put(COMMON_URL, headers=headers, params=params, json=data_payload)
    
    if response.status_code == 200 and response.json().get('status'):
        pass
    else:
        print("Failed to update client. Status code:", name, response.status_code)
        print("Response:", response.text)


def delete_client(cloudshop_id):
    params = {
        "path": f"/data/{COMPANY_ID}/clients/{cloudshop_id}",
        "api": "v3",
        "timezone": "21600",
    }
    response = requests.delete(COMMON_URL, headers=COMMON_HEADERS, params=params)
    if response.status_code == 200 and response.json().get('status'):
        print(cloudshop_id)
        pass
    else:
        print("Failed to delete client. Status code:", response.status_code)
        print("Response:", response.text)


def read_delete_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

if __name__ == "__main__":
    # Read the list of cloudshop_ids to be deleted
    cloudshop_ids = read_delete_list('delete.txt')
    cloudshop_ids = cloudshop_ids
    # cloudshop_ids = cloudshop_ids[:10]  # Limit the number of clients to be deleted
    # Delete clients in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust the number of workers as needed
        # Submit the delete_client task for each cloudshop_id
        executor.map(delete_client, cloudshop_ids)

    print("All delete requests have been submitted.")