import json
import requests
import datetime as dt
from utils.common import write_to_json, read_json, calculate_time
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL
from .docs_utils import handle_sale, handle_return_sale, handle_purchase, handle_return_purchase, handle_movement, handle_change





def get_doc(cloudshop_id):
    params = {
        "path": f"/docs/57c09c3b3ce7d59d048b46c9/{cloudshop_id}",
        "api": "v3",
        "timezone": "32400",
    }

    ok = False
    while not ok:
        response = requests.get(
            COMMON_URL, headers=COMMON_HEADERS, params=params)
        if response.status_code == 200:
            return json.loads(response.text)['data']
            ok = True
        else:
            print("Request failed with status code:", response.status_code)


def load_docs(from_date, to_date):
    params = {
        "path": "/search/docs2/57c09c3b3ce7d59d048b46c9/0/100000",
        "api": "v3",
        "timezone": "32400",
    }

    start_date = from_date
    delta = dt.timedelta(days=10)

    loaded_docs = []

    while start_date < to_date:
        end_date = min(start_date + delta, to_date)
        payload = {
            "start": int(start_date.timestamp()),
            "end": int(end_date.timestamp())
        }
        response = requests.post(
            COMMON_URL, json=payload, params=params, headers=COMMON_HEADERS)
        if response.status_code == 200:
            print(f"{start_date} --- {end_date} --- SUCCESS")
            data = json.loads(response.text)['data']
            loaded_docs.extend(data)
        else:
            print("Request failed with status code:", response.status_code)
        start_date = end_date
        print(end_date)

    with open(f'data/raw/raw_docs.json', 'w', encoding='utf-8') as f:
        json.dump(loaded_docs, f, ensure_ascii=False)
    return 1


def complete_docs(file_name, pack_no):
    with open(f'data/raw/raw_docs.json', 'r', encoding='utf-8') as f:
        loaded_docs = json.load(f)
    completed_docs = []

    batch_size = 2000
    from_index = int(pack_no) * batch_size
    # to_index = min((int(pack_no) + 1) * batch_size, len(loaded_docs))
    to_index = len(loaded_docs)
    print(f"Total: {len(loaded_docs)}/ {from_index} to {to_index}")
    for i, doc in enumerate(loaded_docs[from_index:to_index]):
        cloudshop_id = doc['_id']
        try:
            ok = False
            for _ in range(100):
                try:
                    doc = get_doc(cloudshop_id)
                    completed_docs.append(doc[0])
                    ok = True
                    break
                except:
                    pass
            if ok:
                print(
                    f'Pack no: {pack_no}/// {from_index + i} of {to_index} completed, {cloudshop_id}')
            else:
                print("Failed to get doc", cloudshop_id)
        except:
            print("Failed to get doc", cloudshop_id)
    with open(f'data/raw/{file_name}_{pack_no}.json', 'w', encoding='utf-8') as f:
        json.dump(completed_docs, f, ensure_ascii=False)
    return 1


def clean_docs(file_name, pack_no):
    # response_data = read_json('data/raw/raw_docs.json')
    with open(f'data/raw/{file_name}_{pack_no}.json', 'r', encoding='utf-8') as f:
        completed_docs = json.load(f)
    cleaned_docs = []
    cnt = 0
    stats = {
        'sales_count': 0,
        'return_sales_count': 0,
        'purchases_count': 0,
        'return_purchases_count': 0,
        'movements_count': 0,
        'changes_count': 0,
    }
    for thing in completed_docs:
        doc = {}
        ok = False
        curr = thing['_id']
        if thing['type'] == 'sales':
            doc = handle_sale(thing)
            stats['sales_count'] += 1
            ok = True
        if thing['type'] == 'return_sales':
            doc = handle_return_sale(thing)
            stats['return_sales_count'] += 1
            ok = True
        if thing['type'] == 'purchases':
            doc = handle_purchase(thing)
            stats['purchases_count'] += 1
            ok = True
        if thing['type'] == 'movements':
            doc = handle_movement(thing)
            stats['movements_count'] += 1
            ok = True
        if thing['type'] == 'return_purchases':
            doc = handle_return_purchase(thing)
            stats['return_purchases_count'] += 1
            ok = True
        if thing['type'] == 'changes':
            if isinstance(thing['products'], list):
                doc = handle_change(thing)
                stats['changes_count'] += 1
                ok = True
        if ok:
            #### ADDITIONAL FIELDS ####
            doc['shift_id'] = thing.get('_shift', None)
            doc['register_id'] = thing.get('_register', None)
            doc['status'] = thing['status']
            try:
                doc['comment'] = thing['comment'] or ''
            except:
                doc['comment'] = ''
            cleaned_docs.append(doc)
            cnt += 1
    # sort cleaned docs by date
    cleaned_docs = sorted(cleaned_docs, key=lambda x: x['date'])
    with open(f'data/clean/clean_{file_name}_{pack_no}.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_docs, f, ensure_ascii=False)
    print(f"{cnt} scrapped successfully")
    return 1


# def dump_docs(cleaned_docs):
#     docs_api = f'{BASE_URL}/docs/api/mass-create-update'

#     created_count = 0
#     updated_count = 0
#     docs_data = []
#     for i, doc in enumerate(cleaned_docs):
#         docs_data.append(doc)
#         if i % 50 == 49:
#             response = requests.post(docs_api, json=docs_data)
#             try:
#                 statuses = response.json()['statuses']
#                 for stats in statuses:
#                     if stats['action'] == 'create':
#                         created_count += 1
#                     elif stats['action'] == 'update':
#                         updated_count += 1
#                     print(stats)
#                 docs_data = []
#             except:
#                 print(response.status_code, response.json())
#                 break
#     stats = {
#         "Total": updated_count + created_count,
#         "Created Count": created_count,
#         "Updated Count": updated_count
#     }
#     return (1, stats)


def scrape_docs():
    print("================ DOCS ================")

    # ##### LOADING DOCS #######
    from_date = dt.datetime(2024, 1, 19, 0, 0, 0)
    to_date = dt.datetime(2024, 3, 5, 0, 0, 0)
    status = load_docs(from_date, to_date)
    if status == 0:
        print("Failed to load docs")
        return 0
    else:
        print("1) Loaded...")

    ###### COMPLETING DOCS #######
    pack_no = input("Pack no: ")
    file_name = 'new_docs'
    status = complete_docs(file_name, pack_no)
    if status == 0:
        print("Failed to complete docs")
        return 0
    else:
        print("2) Completed...")
    ####### CLEANING DOCS #######
    status = clean_docs(file_name, pack_no)
    if status == 0:
        print("Failed to clean docs")
    else:
        print("3) Cleaned...")

    # ####### DUMPING DOCS #######
    # status, stats = dump_docs(cleaned_docs)
    # if status == 0:
    #     print("Failed to dump docs")
    # else:
    #     print("4) Dumped...")
    #     print(stats)


if __name__ == '__main__':
    scrape_docs()
