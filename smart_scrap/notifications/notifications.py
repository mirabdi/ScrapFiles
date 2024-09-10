import requests
import json
import datetime as dt
import logging 

from config import COMMON_URL, COMMON_HEADERS
from common import calculate_time

from clients import handle_client
from suppliers import handle_supplier
from stores import handle_store
from registers import handle_register
from catalog import handle_catalog

# helpers
def configure_logging():
    # Create a logger and set the level
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)

    # Create separate handlers for info and warning logs
    info_handler = logging.FileHandler('info.log', mode='a')
    warning_handler = logging.FileHandler('warning.log', mode='a')

    # Set the levels for each handler
    info_handler.setLevel(logging.INFO)
    warning_handler.setLevel(logging.WARNING)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s || %(levelname)s || %(message)s')

    # Set the formatter for each handler
    info_handler.setFormatter(formatter)
    warning_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(info_handler)
    logger.addHandler(warning_handler)

def get_state():
    with open(f'data/state.json', 'r', encoding='utf-8') as f:
        state = json.load(f)
    return state['date']

def update_state(date):
    state = {
        'date': date,
    }
    with open(f'data/state.json', 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False)



# main functions
def load_notifications():
    params = {
        "path": "/65cac563e083953843013fc5/notifications/0/1000",
        "api": "v3",
        "timezone": "32400",
    }
    response = requests.get(COMMON_URL, params=params, headers=COMMON_HEADERS)
    loaded_notifications = json.loads(response.text)['data']
    # print(loaded_notifications)
    resources = set()
    for notification in loaded_notifications:
        try:
            resources.add(notification['resource'])
        except:
            print(f"Resource not found: {notification}")
    print(resources)
    with open(f'data/notifications/raw.json', 'w', encoding='utf-8') as f:
        json.dump(loaded_notifications, f, ensure_ascii=False)

def clean_notifications():
    with open(f'data/notifications/raw.json', 'r', encoding='utf-8') as f:
        completed_notifications = json.load(f)
    cleaned_notifications = []

    resources = ['clients', 'suppliers', 'catalog', 'stores', 'register',       'settings_store', 'accounts',  'sales', 'movements', 'purchases', 'changes', 'return_sales']
    for item in completed_notifications:
        # cloudshop_id = item['_id']
        # client_id = item.get('_client', None)
        # user_id = item.get('_user', None)
        resource = item['resource']
        # method = item['method']
        date = calculate_time(item['date'])
        try:
            item['date'] = calculate_time(item['date'])
        except:
            pass
        # type = item['type']
        if resource in resources:
            cleaned_notifications.append(item)
        else:
            print(f"Resource not found: {resource}")
    cleaned_notifications = sorted(cleaned_notifications, key=lambda x: x['date'])
    with open(f'data/notifications/clean.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_notifications, f, ensure_ascii=False)
    return 1

def processing(from_date):
    cleaned_notifications = []
    with open(f'data/notifications/clean.json', 'r', encoding='utf-8') as f:
        cleaned_notifications = json.load(f)
    to_date = from_date
    for item in cleaned_notifications:
        if item['date'] < from_date:
            continue
        if item['resource'] == 'clients':
            handle_client(item)
        if item['resource'] == 'suppliers':
            handle_supplier(item)
        if item['resource'] == 'stores':
            handle_store(item)
        if item['resource'] == 'register':
            handle_register(item)
        if item['resource'] == 'catalog':
            handle_catalog(item)
    

        
        to_date = item['date']
    # convert from string to datetime and add 1 second
    to_date = dt.datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S') + dt.timedelta(seconds=1)
    return f"{to_date}"
    


def scrap_notifications():
    # Configure the logging module in the main script
    configure_logging()

    # get state
    from_date = "2021-02-13 17:46:00"

    # Load and work
    load_notifications()
    clean_notifications()
    to_date = processing(from_date)

    # Update state
    update_state(to_date)


if __name__ == "__main__":
    scrap_notifications()