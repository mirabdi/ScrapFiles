from common import calculate_time
from config import BASE_URL
import datetime as dt
import requests
import json
import logging

def create_update(register):
    registers_api = f'{BASE_URL}/pos/api/registers/create-update/'
    request_data = register
    response = requests.post(registers_api, json=request_data).json()
    if response['status'] != 0:
        logging.warning(f"registers.create_update || {register['name']} || {register['cloudshop_id']} || {response}")
    else:
        logging.info(f"registers.create_update || {register['name']} || {register['cloudshop_id']} || {response}")

def delete(register):
    registers_api = f'{BASE_URL}/pos/api/registers/delete/'
    request_data = register
    response = requests.post(registers_api, json=request_data).json()
    if response['status'] != 0:
        logging.warning(f"registers.delete || {register['name']} || {register['cloudshop_id']} || {response}")
    else:
        logging.info(f"registers.delete || {register['name']} || {register['cloudshop_id']} || {response}")


def handle_register(notification):
    logging.getLogger(__name__)
    user_id = notification['_user']
    method = notification['method']
    item = notification['data']
    cloudshop_id = item['_id']
    store_id = item['_store']
    name = item['name']
    created = calculate_time(item['created'])

    register = {
        'cloudshop_id': cloudshop_id,
        'name': name,
        'created': created,
        'store_id': store_id,
    }
    if method == 'POST' or method == 'PUT':
        create_update(register)
    elif method == 'DELETE':
        delete(register)

