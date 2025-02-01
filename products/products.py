import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import json
import requests
from utils.common import calculate_time
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL


def load_products():
    params = {
        "path": "/data/57c09c3b3ce7d59d048b46c9/catalog/?limit=100000&offset=0",
        "api": "v3",
        "timezone": "32400",
    }

    response = requests.get(COMMON_URL, headers=COMMON_HEADERS, params=params)

    if response.status_code == 200:
        with open(f'{BASE_DIR}/data/raw/raw_products.json', 'w', encoding='utf-8') as f:
            json.dump(json.loads(response.text), f, ensure_ascii=False)
        return 1
        # write_to_json(response.text, 'data/raw/raw_products.json')
    else:
        print("Request failed with status code:", response.status_code)
        return 0


def clean_products():
    with open(f'{BASE_DIR}/data/raw/raw_products.json', 'r', encoding='utf-8') as f:
        response_data = json.load(f)
    responses = response_data['data']

    cleaned_products = []
    cnt = 0
    for thing in responses:
        cloudshop_id = thing['_id']
        name = thing['name']
        barcode = None
        try:
            barcode = thing['barcode']
        except:
            pass
        code = None
        try:
            code = thing['code']
        except:
            pass
        cost = 0
        try:
            cost = thing['cost']
        except:
            pass
        categories = None
        try:
            categories = thing['categories']
        except:
            pass
        supplier_id = None
        try:
            supplier_id = thing['supplier']
        except:
            pass
        purchase = 0
        try:
            purchase = thing['purchase']
        except:
            pass
        price = 0
        try:
            price = thing['price']
        except:
            pass
        supplier_id = None
        try:
            supplier_id = thing['supplier']
        except:
            pass
        discount = 0
        try:
            discount = thing['discount']
        except:
            pass
        created = calculate_time(thing['created'])
        try:
            pics = thing['pic']
        except:
            pics = []
        price = price if price else 0
        purchase = purchase if purchase else 0
        product = {
            'cloudshop_id': cloudshop_id,
            'name': name,
            'barcode': barcode,
            'code': code,
            'cost': cost,
            'categories': categories,
            'purchase': purchase,
            'price': price,
            'supplier_id': supplier_id,
            'discount': discount,
            'created': created,
            'pics': pics,
            'is_added': True
        }
        cleaned_products.append(product)
        cnt += 1
    # order by created string reversed
    


    cleaned_products = sorted(cleaned_products, key=lambda x: x['created'])
    clean_products = cleaned_products[::-1]
    with open(f'{BASE_DIR}/data/clean/clean_products.json', 'w', encoding='utf-8') as f:
        json.dump(clean_products, f, ensure_ascii=False)
    return 1


def dump_products(create_break):
    with open(f'{BASE_DIR}/data/clean/clean_products.json', 'r', encoding='utf-8') as f:
        cleaned_products = json.load(f)
    products_api = f'{BASE_URL}/import/products-api'
    # products = read_json('data/clean/clean_products.json')
    products = cleaned_products
    temp = []
    cnt = 0
    total = 0
    created_count = 0
    updated_count = 0
    for product in products:
        temp.append(product)
        cnt += 1
        if cnt % 300 == 0:
            request_data = {
                'data': temp,
            }
            response = requests.post(products_api, json=request_data).json()
            if response['created_count'] == 0 and create_break:
                break
            total += response['total']
            created_count += response['created_count']
            updated_count += response['updated_count']
            temp = []
            print(f"Total: {total}, Created: {created_count}, Updated: {updated_count}")

    request_data = {
        'data': temp,
    }
    response = requests.post(products_api, json=request_data).json()
    # print(response)
    total += response['total']
    created_count += response['created_count']
    updated_count += response['updated_count']
    stats = {
        "Total": total,
        "Created Count": created_count,
        "Updated Count": updated_count
    }
    return (1, stats)


def scrape_products(skip_load, create_break=False):
    print("================ PRODUCTS ================")
    if not skip_load:
        status = load_products()
        if status == 0:
            print("Failed to load products")
            return 0
        else:
            print("1) Loaded...")
        status = clean_products()
        if status == 0:
            print("Failed to clean products")
        else:
            print("2) Cleaned...")
    status, stats = dump_products(create_break)
    if status == 0:
        print("Failed to dump products")
    else:
        print("3) Dumped...")
        print(stats)


if __name__ == "__main__":
    scrape_products()