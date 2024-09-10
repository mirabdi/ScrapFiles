import json
import requests
from utils.common import write_to_json, read_json, calculate_time
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL


def load_suppliers():
    params = {
        "path": "/data/57c09c3b3ce7d59d048b46c9/suppliers",
        "api": "v3",
        "timezone": "32400",
    }

    response = requests.get(COMMON_URL, headers=COMMON_HEADERS, params=params)

    if response.status_code == 200:
        return (1, response.text)
        # write_to_json(response.text, 'data/raw/raw_suppliers.json')
    else:
        return (0, f"Request failed with status code: {response.status_code}")


def clean_suppliers(loaded_suppliers):
    # response_data = read_json('data/raw/raw_suppliers.json')
    response_data = json.loads(loaded_suppliers)
    responses = response_data['data']

    cleaned_suppliers = []
    cnt = 0
    for thing in responses:
        cloudshop_id = thing['_id']
        name = thing['name']
        created = calculate_time(thing['created'])

        supplier = {
            'cloudshop_id': cloudshop_id,
            'name': name,
            'created': created,
        }
        cleaned_suppliers.append(supplier)
        cnt += 1
    
    cleaned_suppliers = sorted(cleaned_suppliers, key=lambda x: x['created'])
    return (1, cleaned_suppliers)


def dump_suppliers(cleaned_suppliers):
    suppliers_api = f'{BASE_URL}/import/suppliers-api'
    # suppliers = read_json('data/clean/clean_suppliers.json')
    temp = []
    cnt = 0
    total = 0
    created_count = 0
    updated_count = 0
    for supplier in cleaned_suppliers:
        temp.append(supplier)
        cnt += 1
        if cnt % 100 == 0:
            request_data = {
                'data': temp,
            }
            response = requests.post(suppliers_api, json=request_data).json()
            # if response['created_count'] == 0:
            #     break
            total += response['total']
            created_count += response['created_count']
            updated_count += response['updated_count']
            temp = []
    request_data = {
        'data': temp,
    }
    response = requests.post(suppliers_api, json=request_data).json()
    # print(response)
    total += response['total']
    created_count += response['created_count']
    updated_count += response['updated_count']
    stats = {
        "Total": total,
        "Created Count": created_count,
        "Updated Count": updated_count
    }
    return (1, stats)


def scrape_suppliers():
    print("================ SUPPLIERS ================")
    status, loaded_suppliers = load_suppliers()
    if status == 0:
        print("Failed to load suppliers")
        return 0
    else:
        print("1) Loaded...")
    status, cleaned_suppliers = clean_suppliers(loaded_suppliers)
    if status == 0:
        print("Failed to clean suppliers")
    else:
        print("2) Cleaned...")
    status, stats = dump_suppliers(cleaned_suppliers)
    if status == 0:
        print("Failed to dump suppliers")
    else:
        print("3) Dumped...")
        print(stats)
