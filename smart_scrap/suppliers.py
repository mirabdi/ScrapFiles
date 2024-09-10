from common import calculate_time
from config import BASE_URL
import datetime as dt
import requests
import json
import logging

def create_update(supplier):
    suppliers_api = f'{BASE_URL}/parties/api/suppliers/create-update/'
    request_data = supplier
    response = requests.post(suppliers_api, json=request_data).json()
    if response['status'] != 0:
        logging.warning(f"suppliers.create_update || {supplier['name']} || {supplier['cloudshop_id']} || {response}")
    else:
        logging.info(f"suppliers.create_update || {supplier['name']} || {supplier['cloudshop_id']} || {response}")

def delete(supplier):
    suppliers_api = f'{BASE_URL}/parties/api/suppliers/delete/'
    request_data = supplier
    response = requests.post(suppliers_api, json=request_data).json()
    if response['status'] != 0:
        logging.warning(f"suppliers.delete || {supplier['name']} || {supplier['cloudshop_id']} || {response}")
    else:
        logging.info(f"suppliers.delete || {supplier['name']} || {supplier['cloudshop_id']} || {response}")


def handle_supplier(notification):
    logging.getLogger(__name__)
    user_id = notification['_user']
    method = notification['method']
    item = notification['data']
    cloudshop_id = item['_id']
    name = item['name']
    created = calculate_time(item['created'])

    supplier = {
        'cloudshop_id': cloudshop_id,
        'name': name,
        'created': created,
    }
    if method == 'POST' or method == 'PUT':
        create_update(supplier)
    elif method == 'DELETE':
        delete(supplier)



