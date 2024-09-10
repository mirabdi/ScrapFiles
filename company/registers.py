import json
import requests
from utils.common import write_to_json, read_json, calculate_time
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL
import sys


def load_registers():
    params = {
        "path": "/data/57c09c3b3ce7d59d048b46c9/register/?limit=100000&offset=0",
        "api": "v3",
        "timezone": "32400",
    }

    response = requests.get(COMMON_URL, headers=COMMON_HEADERS, params=params)
    if response.status_code == 200:
        with open(f"data/raw/raw_registers.json", 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, ensure_ascii=False)
        return 1
    else:
        print(response.status_code, response.json())


def clean_registers():
    with open(f"data/raw/raw_registers.json", 'r', encoding='utf-8') as f:
        loaded_registers = json.load(f)

    responses = loaded_registers['data']

    cleaned_registers = []
    cnt = 0
    for thing in responses:
        cloudshop_id = thing['_id']
        name = thing['name']
        store_id = thing['_store']
        created = calculate_time(thing['created'])
        updated = calculate_time(thing['updated'])
        register = {
            'cloudshop_id': cloudshop_id,
            'name': name,
            'store_id': store_id,
            'created': created,
            'updated': updated,
        }
        cleaned_registers.append(register)
        cnt += 1

    with open(f'data/clean/clean_registers.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_registers, f, ensure_ascii=False)
    return 1


def dump_registers():
    registers_api = f'{BASE_URL}/import/registers-api'
    # registers = read_json('data/clean/clean_registers.json')
    with open(f"data/clean/clean_registers.json", 'r', encoding='utf-8') as f:
        cleaned_registers = json.load(f)
    temp = []
    cnt = 0
    total = 0
    created_count = 0
    updated_count = 0
    for register in cleaned_registers:
        temp.append(register)
        cnt += 1
        if cnt % 100 == 0:
            request_data = {
                'data': temp,
            }
            response = requests.post(registers_api, json=request_data).json()
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
    response = requests.post(registers_api, json=request_data).json()
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


def scrape_registers():
    # if __name__ == "__main__":
    print("================ REGISTERS ================")
    ###### LOAD REGISTERS ######
    status = 0
    status = load_registers()
    if status == 0:
        print("Failed to load registers")
    else:
        print("1) Loaded...")

    ###### CLEAN REGISTERS ######
    status = 0
    status = clean_registers()
    if status == 0:
        print("Failed to clean registers")
    else:
        print("2) Cleaned...")
    status = dump_registers()
    if status == 0:
        print("Failed to dump registers")
    else:
        print("3) Dumped...")
