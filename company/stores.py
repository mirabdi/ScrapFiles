import json
import requests
from utils.common import write_to_json, read_json, calculate_time
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL
import sys


def load_stores():
    params = {
        "path": "/data/57c09c3b3ce7d59d048b46c9/stores/?limit=100&offset=0",
        "api": "v3",
        "timezone": "21600",
    }
    print("Loading stores from server...")
    response = requests.get(COMMON_URL, headers=COMMON_HEADERS, params=params)
    if response.status_code == 200: 
        with open(f"data/raw/raw_stores.json", 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, ensure_ascii=False)
        return 1
    else:
        print(response.status_code, response.json())


def clean_stores():
    with open(f"data/raw/raw_stores.json", 'r', encoding='utf-8') as f:
        loaded_stores = json.load(f)

    responses = loaded_stores['data']

    cleaned_stores = []
    cnt = 0
    for thing in responses:
        cloudshop_id = thing['_id']
        name = thing['name']
        deleted = calculate_time(thing['deleted'])
        created = calculate_time(thing['created'])
        updated = calculate_time(thing['updated'])
        store = {
            'cloudshop_id': cloudshop_id,
            'name': name,
            'deleted': deleted,
            'created': created,
            'updated': updated,
        }
        cleaned_stores.append(store)
        cnt += 1

    with open(f'data/clean/clean_stores.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_stores, f, ensure_ascii=False)
    return 1


def dump_stores():
    stores_api = f'{BASE_URL}/import/stores-api'
    # stores = read_json('data/clean/clean_stores.json')
    with open(f"data/clean/clean_stores.json", 'r', encoding='utf-8') as f:
        cleaned_stores = json.load(f)
    temp = []
    cnt = 0
    total = 0
    created_count = 0
    updated_count = 0
    for store in cleaned_stores:
        temp.append(store)
        cnt += 1
        if cnt % 100 == 0:
            request_data = {
                'data': temp,
            }
            response = requests.post(stores_api, json=request_data).json()
            print(response)
            if response['created_count'] == 0:
                break
            total += response['total']
            created_count += response['created_count']
            updated_count += response['updated_count']
            temp = []
    request_data = {
        'data': temp,
    }
    response = requests.post(stores_api, json=request_data).json()
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


def scrape_stores():
    # if __name__ == "__main__":
    print("================ STORES ================")
    ###### LOAD STORES ######
    status = 0
    status = load_stores()
    if status == 0:
        print("Failed to load stores")
    else:
        print("1) Loaded...")

    ###### CLEAN STORES ######
    status = 0
    status = clean_stores()
    if status == 0:
        print("Failed to clean stores")
    else:
        print("2) Cleaned...")
    status = dump_stores()
    if status == 0:
        print("Failed to dump stores")
    else:
        print("3) Dumped...")
