from common import calculate_time
from config import BASE_URL
import datetime as dt
import requests
import json
import logging

def product_create_update(product):
    products_api = f'{BASE_URL}/products/api/products/create-update/'
    request_data = product
    response = requests.post(products_api, json=request_data).json()
    if response['status'] != 0:
        logging.warning(f"products.create_update || {product['name']} || {product['cloudshop_id']} || {response}")
    else:
        logging.info(f"products.create_update || {product['name']} || {product['cloudshop_id']} || {response}")

def product_delete(product):
    products_api = f'{BASE_URL}/products/api/products/delete/'
    request_data = product
    response = requests.post(products_api, json=request_data).json()
    if response['status'] != 0:
        logging.warning(f"products.delete || {product['name']} || {product['cloudshop_id']} || {response}")
    else:
        logging.info(f"products.delete || {product['name']} || {product['cloudshop_id']} || {response}")

def handle_product(item, method):
    cloudshop_id = item['_id']
    name = item['name']
    barcode = item.get('barcode', None)
    code = item.get('code', None)
    cost = item.get('cost', 0)
    categories = item.get('categories', [])
    supplier_id = item.get('supplier', None)
    group_id = item.get('id_group', 0)
    purchase = item.get('purchase', 0)
    price = item.get('price', 0)
    discount = item.get('discount', 0)
    try:
        created = calculate_time(item['created'])
    except:
        created = calculate_time(item['created_ms'])
    pics = item.get('pic', [])

    product = {
        'cloudshop_id': cloudshop_id,
        'name': name,
        'barcode': barcode,
        'code': code,
        'cost': cost,
        'categories': categories,
        'group_id': group_id,
        'purchase': purchase,
        'price': price,
        'supplier_id': supplier_id,
        'discount': discount,
        'created': created,
        'pics': pics
    }
    if method == 'POST' or method == 'PUT':
        product_create_update(product)
    elif method == 'DELETE':
        product_delete(product)

def group_create_update(group):
    groups_api = f'{BASE_URL}/products/api/groups/create-update/'
    request_data = group
    response = requests.post(groups_api, json=request_data).json()
    if response['status'] != 0:
        logging.warning(f"groups.create_update || {group['name']} || {group['cloudshop_id']} || {response}")
    else:
        logging.info(f"groups.create_update || {group['name']} || {group['cloudshop_id']} || {response}")

def group_delete(group):
    groups_api = f'{BASE_URL}/products/api/groups/delete/'
    request_data = group
    response = requests.post(groups_api, json=request_data).json()
    if response['status'] != 0:
        logging.warning(f"groups.delete || {group['name']} || {group['cloudshop_id']} || {response}")
    else:
        logging.info(f"groups.delete || {group['name']} || {group['cloudshop_id']} || {response}")



def handle_group(item, method):
    cloudshop_id = item['_id']
    name = item['name']
    group_id = item.get('id_group', 0)
    try:
        created = calculate_time(item['created'])
    except:
        created = calculate_time(item['created_ms'])
    group = {
        'cloudshop_id': cloudshop_id,
        'name': name,
        'group_id': group_id,
        'created': created,
    }
    if method == 'POST' or method == 'PUT':
        group_create_update(group)
    elif method == 'DELETE':
        group_delete(group)


def handle_catalog(notification):
    user_id = notification['_user']
    method = notification['method']
    item = notification['data']
    # try:
    tpy = item.get("type", None)
    if tpy == 'inventory':
        handle_product(item, method)
    elif tpy == 'group':
        handle_group(item, method)
    else:
        # print(f"Unknown type: {tpy}", item)
        pass
    # except KeyError:
    #     print(item)