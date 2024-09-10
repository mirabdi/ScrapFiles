from common import calculate_time
from config import BASE_URL
import datetime as dt
import requests
import json
import logging

def create_update(client):
    clients_api = f'{BASE_URL}/parties/api/clients/create-update/'
    request_data = client
    response = requests.post(clients_api, json=request_data).json()
    if response['status'] != 0:
        logging.warning(f"clients.create_update || {client['name']} || {client['cloudshop_id']} || {response}")
    else:
        logging.info(f"clients.create_update || {client['name']} || {client['cloudshop_id']} || {response}")

def delete(client):
    clients_api = f'{BASE_URL}/parties/api/clients/delete/'
    request_data = client
    response = requests.post(clients_api, json=request_data).json()
    if response['status'] != 0:
        logging.warning(f"clients.delete || {client['name']} || {client['cloudshop_id']} || {response}")
    else:
        logging.info(f"clients.delete || {client['name']} || {client['cloudshop_id']} || {response}")

def handle_client(notification):
    user_id = notification['_user']
    method = notification['method']
    item = notification['data']
    cloudshop_id = item.get('_id', None)
    name = item.get('name', None)
    gender = item.get('sex', None)
    created = calculate_time(item.get('created', None))
    discount = item.get('discount', 0)
    discount_card = item.get('discount_card', None)
    phone = item.get('phones', [None])[0]
    birthday = calculate_time(item.get('bday', None))
    if birthday:
        birthday = f"{dt.datetime.strptime(birthday, '%Y-%m-%d %H:%M:%S').date()}"

    description = item.get('description', None)

    client = {
        'cloudshop_id': cloudshop_id,
        'name': name,
        'gender': gender,
        'created': created,
        'discount': discount,
        'discount_card': discount_card,
        'phone': phone,
        'birthday': birthday,
        'description': description,
    }
    if method == 'POST' or method == 'PUT':
        create_update(client)
    elif method == 'DELETE':
        delete(client)


# cloudshop_id
# name 
# gender 
# created
# discount
# discount_card
# phone


# cloudshop fields:
# | Field               | Description                     | Data Type              |
# |---------------------|---------------------------------|------------------------|
# | _id                 | Cloudshop ID                   | string                 |
# | name                | Name of client                 | string                 |
# | type                | Type                            | string                 |
# | phones              | List of phones                  | list                   |
# | emails              | List of emails                  | list                   |
# | bday                | Birthday                        | integer                |
# | discount            | Discount                        | integer                |
# | discount_card       | Discount                        | string                 |
# | sex                 | Gender                          | string                 |
# | enable_savings      | Savings enabled                 | boolean                |
# | default             | Default                         | boolean                |
# | address             | Address                         | dictionary             |
# | details             | Details                         | list                   |
# | bank_details        | Bank details                    | list                   |
# | _user               | User ID                         | string                 |
# | _client             | Client ID                       | string                 |
# | created             | Creation timestamp              | integer                |
# | updated             | Update timestamp                | integer                |
# | deleted             | Deleted                         | boolean                |
# | _app                | App                             | string                 |
# | created_ms          | Creation timestamp (milliseconds)| float                  |
# | info_user_id        | User ID in info                 | string                 |
# | info_user_name      | User name in info                | string                 |
# | info_user_email     | User email in info               | string                 |
# | info_user_phone     | User phone in info               | string                 |
# | info_user_pic       | User pic in info                 | NoneType or string     |
# | info_user_created   | User creation timestamp in info  | integer                |
