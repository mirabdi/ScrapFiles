import json
import requests
from utils.common import write_to_json, read_json, calculate_time, clean_phone
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL


def load_clients():
    params = {
        "path": "/data/57c09c3b3ce7d59d048b46c9/clients/?limit=100000&offset=0",
        "api": "v3",
        "timezone": "32400",
    }

    response = requests.get(COMMON_URL, headers=COMMON_HEADERS, params=params)


    if response.status_code == 200:
        loaded_clients = json.loads(response.text)['data']
        with open(f'data/raw/raw_clients.json', 'w', encoding='utf-8') as f:
            json.dump(loaded_clients, f, ensure_ascii=False)
        return 1
    else:
        return (0, f"Request failed with status code: {response.status_code}")


def update_client(cloudshop_id, name):
    params = {
        "path": f"/data/57c09c3b3ce7d59d048b46c9/clients/{cloudshop_id}",
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
        print("Updated client:", name)
    else:
        print("Failed to update client. Status code:", name, response.status_code)
        print("Response:", response.text)
        raise Exception(f"Failed to update client {name} ID:{cloudshop_id} with status code {response.status_code}")



def validate_client():
    with open(f'data/raw/raw_clients.json', 'r', encoding='utf-8') as f:
        loaded_clients = f.read()
    response_data = json.loads(loaded_clients)
    responses = response_data

    for thing in responses:
        loyalty_type = thing.get('loyalty_type', None)
        enable_savings = thing.get('enable_savings', False)
        bonus_balance = thing.get('bonus_balance', None)
        bonus_spent = thing.get('bonus_spent', None)

        if enable_savings or (loyalty_type is None or bonus_balance is None or bonus_spent is None):
            update_client(thing['_id'], thing['name'])
            print(f"Updated client {thing['name']} with missing data")
            thing['loyalty_type'] = 'bonus'
            thing['enable_savings'] = False
            thing['bonus_balance'] = 0
            thing['bonus_spent'] = 0
    
    with open(f'data/raw/raw_clients.json', 'w', encoding='utf-8') as f:
        json.dump(responses, f, ensure_ascii=False)

    return 1



def clean_clients():
    with open(f'data/raw/raw_clients.json', 'r', encoding='utf-8') as f:
        loaded_clients = f.read()
    response_data = json.loads(loaded_clients)
    responses = response_data

    cleaned_clients = []
    cnt = 0
    for thing in responses:
        cloudshop_id = thing['_id']
        name = thing.get('name', None)
        if name:
            name = name.strip()
        gender = thing.get('sex', 'female')
        if not gender:
            gender = 'female'
        created = calculate_time(thing['created'])
        birthday = thing.get('birthday')
        if birthday:
            birthday = calculate_time(birthday).split(' ')[0]
        discount_percent = thing.get('discount_percent', None)
        discount_card = thing.get('discount_card', None)
        phones = thing.get('phones', [None])
        phone = phones[0] if phones else None
        loyalty_type = thing.get('loyalty_type', None)
        enable_savings = thing.get('enable_savings', None)
        bonus_balance = thing.get('bonus_balance', None)
        bonus_spent = thing.get('bonus_spent', None)
        cashback_rate = thing.get('cashback_rate', 5)

        if bonus_balance is None or bonus_spent is None or cashback_rate is None:
            raise Exception(f"Failed to clean client {name} ID:{cloudshop_id} with missing data")
        phone = clean_phone(phone)
        client = {
            'cloudshop_id': cloudshop_id,
            'name': name,
            'gender': gender,
            'created': created,
            'discount_percent': discount_percent,
            'discount_card': discount_card,
            'phone': phone,
            'enable_savings': enable_savings,
            'loyalty_type': loyalty_type,
            'bonus_balance': bonus_balance,
            'bonus_spent': bonus_spent,
            'cashback_rate': cashback_rate,
            'birthday': birthday,
        }
        cleaned_clients.append(client)
        cnt += 1
    cleaned_clients = sorted(cleaned_clients, key=lambda x: x['created'])
    cleaned_clients = cleaned_clients[::-1]
    with open(f'data/clean/clean_clients.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_clients, f, ensure_ascii=False)
    return 1


def merge_clients():
    # Load the cleaned clients JSON data
    with open(f'data/clean/clean_clients.json', 'r', encoding='utf-8') as f:
        cleaned_clients = json.load(f)
    
    # Dictionary to store merged clients by phone number
    merged_clients = {}
    
    for client in cleaned_clients:
        phone = client.get('phone')
        if not phone:
            continue
        
        if phone in merged_clients:
            # If the phone number already exists, merge the bonus balances and spent
            merged_clients[phone]['bonus_balance'] += client.get('bonus_balance', 0)
            merged_clients[phone]['bonus_spent'] += client.get('bonus_spent', 0)
        else:
            # Otherwise, add the client to the merged clients dictionary
            merged_clients[phone] = {
                'cloudshop_id': client['cloudshop_id'],
                'name': client['name'],
                'gender': client['gender'],
                'created': client['created'],
                'discount_percent': client.get('discount_percent'),
                'discount_card': client.get('discount_card'),
                'phone': client['phone'],
                'enable_savings': client.get('enable_savings'),
                'loyalty_type': client.get('loyalty_type'),
                'bonus_balance': client.get('bonus_balance', 0),
                'bonus_spent': client.get('bonus_spent', 0),
                'cashback_rate': client.get('cashback_rate'),
                'birthday': client.get('birthday')
            }

    # Convert the merged_clients dictionary back to a list
    merged_clients_list = list(merged_clients.values())

    # Save the merged clients data to a new file (optional)
    with open(f'data/clean/clean_clients.json', 'w', encoding='utf-8') as f:
        json.dump(merged_clients_list, f, ensure_ascii=False, indent=4)

    return 1


def dump_clients(create_break):
    with open(f'data/clean/clean_clients.json', 'r', encoding='utf-8') as f:
        cleaned_clients = json.load(f)
    clients_api = f'{BASE_URL}/import/clients-api'
    # clients = read_json('data/clean/clean_clients.json')
    temp = []
    cnt = 0
    total = 0
    created_count = 0
    updated_count = 0
    for client in cleaned_clients:
        temp.append(client)
        cnt += 1
        if cnt % 300 == 0:
            request_data = {
                'data': temp,
            }
            response = requests.post(clients_api, json=request_data).json()
            print(f"Total: {total}, Created: {created_count}, Updated: {updated_count}")
            if response['created_count'] == 0 and create_break:
                break
            total += response['total']
            created_count += response['created_count']
            updated_count += response['updated_count']
            temp = []
    request_data = {
        'data': temp,
    }
    response = requests.post(clients_api, json=request_data).json()
    # print(response)
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


def scrape_clients(skip_load, create_break=True):
    print("================ CLIENTS ================")
    if not skip_load:
        status = load_clients()
        if status == 0:
            print("Failed to load clients")
            return 0
        else:
            print("1) Loaded...")

    status = validate_client()
    if status == 0:
        print("Failed to validate clients")
    else:
        print("2) Validated...")
    
    status = clean_clients()
    if status == 0:
        print("Failed to clean clients")
    else:
        print("2) Cleaned...")

    status = merge_clients()
    # return

    status = dump_clients(create_break)
    if status == 0:
        print("Failed to dump clients")
    else:
        print("3) Dumped...")