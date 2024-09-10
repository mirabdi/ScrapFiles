from common import calculate_time
from config import BASE_URL
import datetime as dt
import requests
import json
import logging

def create_update(store):
    stores_api = f'{BASE_URL}/api/stores/create-update/'
    request_data = store
    response = requests.post(stores_api, json=request_data).json()
    if response['status'] != 0:
        logging.warning(f"stores.create_update || {store['name']} || {store['cloudshop_id']} || {response}")
    else:
        logging.info(f"stores.create_update || {store['name']} || {store['cloudshop_id']} || {response}")

def delete(store):
    stores_api = f'{BASE_URL}/api/stores/delete/'
    request_data = store
    response = requests.post(stores_api, json=request_data).json()
    if response['status'] != 0:
        logging.warning(f"stores.delete || {store['name']} || {store['cloudshop_id']} || {response}")
    else:
        logging.info(f"stores.delete || {store['name']} || {store['cloudshop_id']} || {response}")


def handle_store(notification):
    logging.getLogger(__name__)
    user_id = notification['_user']
    method = notification['method']
    item = notification['data']
    cloudshop_id = item['_id']
    name = item['name']
    created = calculate_time(item['created'])

    store = {
        'cloudshop_id': cloudshop_id,
        'name': name,
        'created': created,
    }
    if method == 'POST' or method == 'PUT':
        create_update(store)
    elif method == 'DELETE':
        delete(store)

