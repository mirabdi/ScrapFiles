import json
import requests
import datetime as dt
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL
from utils.common import calculate_time

def load_accounts():
    print("Loading accounts from server...")
    params = {
        "path": "/data/57c09c3b3ce7d59d048b46c9/accounts",  # Modify the endpoint
        "api": "v3",
        "timezone": "32400",
    }

    response = requests.get(COMMON_URL, params=params, headers=COMMON_HEADERS)
    
    if response.status_code == 200:
        print("Accounts loaded successfully.")
        accounts_data = json.loads(response.text)['data']
        with open('data/raw/raw_accounts.json', 'w', encoding='utf-8') as f:
            json.dump(accounts_data, f, ensure_ascii=False)
        return 1
    else:
        print("Request failed with status code:", response.status_code)
        return 0

def clean_accounts():
    loaded_accounts = []

    with open('data/raw/raw_accounts.json', 'r', encoding='utf-8') as f:
        loaded_accounts = json.load(f)

    cleaned_accounts = []

    for account in loaded_accounts:
        try:
            name = account['name']
            cloudshop_id = account['_id']
            style = account.get('type', None)
            address = account.get('address', None)
            user_id = account.get('_user', None)

            register_id = account.get('register_id', None)
            income = account['balance']['income']
            outcome = account['balance']['outcome']
            balance = account['balance']['balance']
            created = calculate_time(account['created'])
            updated = calculate_time(account['updated'])
            deleted = account['deleted']
            include = account['include']

            cleaned_account = {
                'cloudshop_id': cloudshop_id,
                'name': name,
                'style': style,
                'address': address,
                'user_id': user_id,
                'register_id': register_id,
                'income': income,
                'outcome': outcome,
                'balance': balance,
                'created': created,
                'updated': updated,
                'deleted': deleted,
                'include': include,
            }

            cleaned_accounts.append(cleaned_account)
        except Exception as e:
            print(e)
            print(account)
            break

    with open('data/clean/clean_accounts.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_accounts, f, ensure_ascii=False)

    return 1


def dump_accounts():
    with open('data/clean/clean_accounts.json', 'r', encoding='utf-8') as f:
        cleaned_accounts = json.load(f)

    accounts_api = f'{BASE_URL}/import/accounts-api'  # Modify the API endpoint

    temp = []
    cnt = 0
    total = 0
    created_count = 0
    updated_count = 0

    for account in cleaned_accounts:
        temp.append(account)
        cnt += 1

        if cnt % 100 == 0:
            request_data = {
                'data': temp,
            }
            response = requests.post(accounts_api, json=request_data).json()

            if response['created_count'] == 0:
                break

            total += response['total']
            created_count += response['created_count']
            updated_count += response['updated_count']
            temp = []

    request_data = {
        'data': temp,
    }
    response = requests.post(accounts_api, json=request_data).json()
    total += response['total']
    created_count += response['created_count']
    updated_count += response['updated_count']

    stats = {
        "Total": total,
        "Created Count": created_count,
        "Updated Count": updated_count
    }
    print(stats)
    return 1


def scrape_accounts():
    print("=============== ACCOUNTS ===============")

    ########### Loading accounts
    status = load_accounts()
    if status == 1:
        print("Loading accounts completed successfully.")
    else:
        print("Loading accounts failed.")

    ########### Cleaning accounts
    status = clean_accounts()
    if status == 1:
        print("Cleaning accounts completed successfully.")
    else:
        print("Cleaning accounts failed.")

    # ########## Dumping accounts
    status = dump_accounts()
    if status == 1:
        print("Dumping accounts completed successfully.")
    else:
        print("Dumping accounts failed.")

if __name__ == "__main__":
    scrape_accounts()
