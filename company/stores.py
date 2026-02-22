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

def read_stores():
    return [{'cloudshop_id': '667a67de8d522538ee0ba760', 'name': 'OFF PRICE №8', 'deleted': None, 'created': '2024-06-25 12:46:54', 'updated': '2025-08-17 21:09:06'}, {'cloudshop_id': '60a1ffac0bd70c60721c5c99', 'name': 'Балапан ЖА №3', 'deleted': None, 'created': '2021-05-17 11:31:24', 'updated': '2025-08-17 20:53:40'}, {'cloudshop_id': '617be0fd23e410238456d59f', 'name': '№-01 Osnovnoy sklad', 'deleted': None, 'created': '2021-10-29 17:54:37', 'updated': '2025-08-17 20:50:30'}, {'cloudshop_id': '68667cf3d9f22a70511317c4', 'name': 'Промежуточный Флагман', 'deleted': None, 'created': '2025-07-03 18:52:03', 'updated': '2025-07-03 18:52:03'}, {'cloudshop_id': '67e6969e538f850166653263', 'name': 'Сезонное хранение', 'deleted': None, 'created': '2025-03-28 18:31:26', 'updated': '2025-03-28 18:31:26'}, {'cloudshop_id': '6187a2f023e410447a333bd0', 'name': 'Балапан Анар №4', 'deleted': None, 'created': '2021-11-07 15:57:04', 'updated': '2024-07-22 09:52:03'}, {'cloudshop_id': '57c09c3d3ce7d59d048b46ca', 'name': 'Балапан Ош №1', 'deleted': None, 'created': '2016-08-27 01:45:01', 'updated': '2024-04-07 14:40:54'}, {'cloudshop_id': '6534e92e6b78a2722e0a1b13', 'name': 'Балапан Фрунзенский №7', 'deleted': None, 'created': '2023-10-22 15:19:42', 'updated': '2023-11-15 23:34:36'}, {'cloudshop_id': '61fcfbe56fd83334d906684b', 'name': 'Балапан Масалиева №5', 'deleted': None, 'created': '2022-02-04 16:11:49', 'updated': '2023-07-18 11:25:41'}, {'cloudshop_id': '637b680b51c3772c3270c50c', 'name': 'Балапан Узген №6', 'deleted': None, 'created': '2022-11-21 17:59:07', 'updated': '2022-11-24 14:09:13'}, {'cloudshop_id': '608931190bd70c702d0dbf6c', 'name': 'Балапашка №2', 'deleted': None, 'created': '2021-04-28 15:55:37', 'updated': '2022-06-04 23:17:54'}]

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
