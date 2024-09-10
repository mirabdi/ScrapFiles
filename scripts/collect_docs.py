import json
import datetime as dt


def calculate_time(timestamp):
    timestamp = dt.datetime.fromtimestamp(timestamp)
    return f"{timestamp}"


def handle_sale(thing):
    number = thing['number']
    cloudshop_id = thing['_id']
    store = thing['from']['_id']
    client = thing['to']['_id']
    date = calculate_time(thing['date'])
    created = calculate_time(thing['created'])
    response = {
        'style': 'sales',
        'number': number,
        'cloudshop_id': cloudshop_id,
        'store': store,
        'date': date,
        'created': created,
        'client': client,
    }
    products = []
    for item in thing['products']:
        cloudshop_id = item['_id']
        quantity = -item['qty']
        sum = item['sum']
        sub = item['sub']
        price = item['price']
        discount_sum = item['discount_sum']
        discount_percent = item['discount_percent']
        product = {
            'cloudshop_id': cloudshop_id,
            'quantity': abs(quantity),
            'sum': abs(sum),
            'sub': abs(sub),
            'price': abs(price),
            'discount_sum': discount_sum,
            'discount_percent': discount_percent,
        }
        products.append(product)
    response['positions'] = products
    return response


def handle_return_sale(thing):
    number = thing['number']
    cloudshop_id = thing['_id']
    store = thing['to']['_id']
    client = thing['from']['_id']
    date = calculate_time(thing['date'])
    created = calculate_time(thing['created'])
    response = {
        'style': 'return_sales',
        'number': number,
        'cloudshop_id': cloudshop_id,
        'store': store,
        'date': date,
        'created': created,
        'client': client,
    }
    products = []
    for item in thing['products']:
        cloudshop_id = item['_id']
        quantity = item['qty']
        sum = item['sum']
        sub = item['sub']
        price = item['price']
        discount_sum = item['discount_sum']
        discount_percent = item['discount_percent']
        product = {
            'cloudshop_id': cloudshop_id,
            'quantity': abs(quantity),
            'sum': abs(sum),
            'sub': abs(sub),
            'price': abs(price),
            'discount_sum': discount_sum,
            'discount_percent': discount_percent,
        }
        products.append(product)
    response['positions'] = products
    return response


def handle_purchase(thing):
    number = thing['number']
    cloudshop_id = thing['_id']
    store = thing['to']['_id']
    supplier = thing['from']['_id']
    date = calculate_time(thing['date'])
    created = calculate_time(thing['created'])
    response = {
        'style': 'purchases',
        'number': number,
        'cloudshop_id': cloudshop_id,
        'store': store,
        'supplier': supplier,
        'date': date,
        'created': created,
    }
    products = []
    for item in thing['products']:
        cloudshop_id = item['_id']
        quantity = item['qty']
        sum = item['sum']
        sub = item['sub']
        price = item['price']
        product = {
            'cloudshop_id': cloudshop_id,
            'quantity': abs(quantity),
            'sum': abs(sum),
            'sub': abs(sub),
            'price': abs(price),
        }
        products.append(product)
    response['positions'] = products
    return response


def handle_return_purchase(thing):
    number = thing['number']
    cloudshop_id = thing['_id']
    store = thing['from']['_id']
    supplier = thing['to']['_id']
    date = calculate_time(thing['date'])
    created = calculate_time(thing['created'])
    response = {
        'style': 'return_purchases',
        'number': number,
        'cloudshop_id': cloudshop_id,
        'store': store,
        'supplier': supplier,
        'date': date,
        'created': created,
    }
    products = []
    for item in thing['products']:
        cloudshop_id = item['_id']
        quantity = -item['qty']
        sum = item['sum']
        sub = item['sub']
        price = item['price']
        product = {
            'cloudshop_id': cloudshop_id,
            'quantity': abs(quantity),
            'sum': abs(sum),
            'sub': abs(sub),
            'price': abs(price),
        }
        products.append(product)
    response['positions'] = products
    return response


def handle_movement(thing):
    number = thing['number']
    cloudshop_id = thing['_id']
    to_store = thing['to']['_id']
    from_store = thing['from']['_id']
    date = calculate_time(thing['date'])
    created = calculate_time(thing['created'])
    response = {
        'style': 'movements',
        'number': number,
        'cloudshop_id': cloudshop_id,
        'from_store': from_store,
        'to_store': to_store,
        'date': date,
        'created': created,
    }
    products = []
    for item in thing['products']:
        cloudshop_id = item['_id']
        quantity = item['qty']
        sum = item['sum']
        sub = item['sub']
        price = item['price']
        discount_sum = item['discount_sum']
        discount_percent = item['discount_percent']
        product = {
            'cloudshop_id': cloudshop_id,
            'quantity': abs(quantity),
            'price': abs(price),
        }
        products.append(product)
    response['positions'] = products
    return response


def handle_change(thing):
    number = thing['number']
    cloudshop_id = thing['_id']
    store = thing['from']['_id']
    date = calculate_time(thing['date'])
    created = calculate_time(thing['created'])
    sub_style = thing.get('sub_type', 'correction')
    response = {
        'style': 'changes',
        'sub_style': sub_style,
        'number': number,
        'cloudshop_id': cloudshop_id,
        'store': store,
        'date': date,
        'created': created,
    }
    products = []
    for item in thing['products']:
        cloudshop_id = item['_id']
        quantity = item['qty']
        price = item['price']
        product = {
            'cloudshop_id': cloudshop_id,
            'quantity': abs(quantity),
            'price': abs(price),
        }
        products.append(product)
    response['positions'] = products
    return response


def handle(thing):
    response = thing
    print(thing['products'] is list)
    return response


def clean_docs(completed_docs):
    # response_data = read_json('data/raw/raw_docs.json')

    cleaned_docs = []
    cnt = 0
    for i in range(len(completed_docs)):
        try:
            thing = completed_docs[i]
        except:
            continue
        doc = {}
        ok = False
        curr = thing['_id']
        if thing['type'] == 'sales':
            doc = handle_sale(thing)
            ok = True
        if thing['type'] == 'return_sales':
            doc = handle_return_sale(thing)
            ok = True
        if thing['type'] == 'purchases':
            doc = handle_purchase(thing)
            ok = True
        if thing['type'] == 'movements':
            doc = handle_movement(thing)
            ok = True
        if thing['type'] == 'return_purchases':
            doc = handle_return_purchase(thing)
            ok = True
        if thing['type'] == 'changes':
            if isinstance(thing['products'], list):
                doc = handle_change(thing)
                ok = True
        if ok:
            cleaned_docs.append(doc)
            cnt += 1

        with open(f"../data/clean/clean_docs.json", 'w', encoding='utf-8') as f:
            json.dump(cleaned_docs, f, ensure_ascii=False)

    print(f"{cnt} scrapped successfully")
    return (1, cleaned_docs)


all_docs = []
file_name = input("Enter file name: ")
pack_count = int(input("Enter pack count: "))
for pack_no in range(pack_count):
    with open(f'../data/completed/{file_name}_{pack_no}.json',  'r', encoding='utf-8') as f:
        data = json.load(f)
    all_docs.extend(data)
    # do something with doc
all_docs = sorted(all_docs, key=lambda x: x['date'])
print(len(all_docs))
with open(f"../data/completed/{file_name}.json", 'w', encoding='utf-8') as f:
    json.dump(all_docs, f, ensure_ascii=False)
