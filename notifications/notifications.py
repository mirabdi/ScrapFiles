import json
import requests
import datetime as dt
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL
from utils.common import calculate_time


def load_notifications_from_server():
    print("Loading notifications from server...")
    params = {
        "path": "/57c09c3b3ce7d59d048b46c9/notifications/0/10000",
        "api": "v3",
        "timezone": "32400",
    }
    loaded_notifications = []
    response = requests.get(COMMON_URL, params=params, headers=COMMON_HEADERS)
    if response.status_code == 200:
        loaded_notifications = json.loads(response.text)['data']
    
    resources = set()
    for notification in loaded_notifications:
        resources.add(notification['resource'])
    print(resources)
    with open(f'data/raw/raw_notifications.json', 'w', encoding='utf-8') as f:
        json.dump(loaded_notifications, f, ensure_ascii=False)
    return 1


def clean_notifications():
    with open(f'data/raw/raw_notifications.json', 'r', encoding='utf-8') as f:
        completed_notifications = json.load(f)
    cleaned_notifications = []

    resources = ['clients', 'accounts', 'suppliers', 'movements', 'purchases', 'changes', 'register', 'sales', 'settings_store', 'catalog', 'return_sales']
    for thing in completed_notifications:
        # cloudshop_id = thing['_id']
        # client_id = thing.get('_client', None)
        # user_id = thing.get('_user', None)
        resource = thing['resource']
        # method = thing['method']
        date = calculate_time(thing['date'])
        # type = thing['type']
        if resource in resources:
            cleaned_notifications.append(thing)
            resources.remove(resource)
    cleaned_notifications = sorted(cleaned_notifications, key=lambda x: x['date'])
    with open(f'data/clean/clean_notifications.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_notifications, f, ensure_ascii=False)
    return 1


def dump_notifications():
    notifications_api = f'{BASE_URL}/import/notifications-api'
    with open(f"data/clean/clean_notifications.json", 'r', encoding='utf-8') as f:
        cleaned_notifications = json.load(f)
    temp = []
    cnt = 0
    total = 0
    created_count = 0
    updated_count = 0
    for notification in cleaned_notifications:
        temp.append(notification)
        cnt += 1
        if cnt % 100 == 0:
            request_data = {
                'data': temp,
            }
            response = requests.post(notifications_api, json=request_data).json()
            print(response)
            # if response['created_count'] == 0:
            #     break
            # total += response['total']
            # created_count += response['created_count']
            # updated_count += response['updated_count']
            temp = []
    request_data = {
        'data': temp,
    }
    response = requests.post(notifications_api, json=request_data).json()
    print(response)
    return 1


def scrape_notifications(from_date, to_date):
    print("=================== SCRAPING NOTIFICATIONS STARTED ==============")
    ##### LOAD NOTIFICATIONS #####
    # status = 0
    # status = load_notifications_from_server(from_date, to_date)
    # if status == 0:
    #     print("Loading notifications from server failed")
    # else:
    #     print("Loading notifications from server finished")


    # ##### CLEANING NOTIFICATIONS #####
    status = 0
    status = clean_notifications()
    if status == 0:
        print("Cleaning notifications failed")
    else:
        print("Cleaning notifications finished")

    # #### DUMPING NOTIFICATIONS #####
    # status = 0
    # status = dump_notifications()
    # if status == 0:
    #     print("Dumping notifications failed")
    # else:
    #     print("Dumping notifications finished")
