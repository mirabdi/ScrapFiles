import json
import openpyxl
import requests
from config import COMMON_HEADERS, COMMON_URL, BASE_URL
import concurrent.futures

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
        pass
    else:
        print("Failed to delete client. Status code:", response.status_code)
        print("Response:", response.text)



if __name__ == "__main__":
    # Load the Excel file
    data = load_client("5b7556be3ce7d5ba0b8b4567")  
    print(data)