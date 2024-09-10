import json
import requests
import os
import datetime as dt
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL
import concurrent.futures
from .docs_utils import handle_sale, handle_return_sale, handle_purchase, handle_return_purchase, handle_movement, handle_change, emps, stores

errors = []
def get_consultant(doc):
    store_id = doc.get('store', None)
    comment = doc.get('comment', '')
    if '@' in comment:
        username = comment.split('@')[1].split()[0]
        if username in emps:
            return username
    
    consultant_name = ''.join(filter(str.isalpha, comment.split(' ')[0].strip())).lower()

    if len(consultant_name) == 0:
        return None
    if store_id:
        store_name = stores[store_id]['name']
        store_city = stores[store_id]['city']
    else:
        store_name = None
        store_city = None
    matches = []
    for username, details in emps.items():
        if consultant_name in details["versions"]:
            matches.append(username)
    if len(matches) > 1:
        for username, details in emps.items():
            if store_id == details["store_id"]:
                store_name = details["store_name"]
            if details["city"] == store_city and consultant_name in details["versions"]:
                return username
    elif len(matches) == 1:
        return matches[0]
    print(f"Store name {store_name}: store id: {store_id} with name version '{consultant_name}' does not match any existing entry. {comment}")
    return None


def get_doc(cloudshop_id):
    params = {
        "path": f"/docs/57c09c3b3ce7d59d048b46c9/{cloudshop_id}",
        "api": "v3",
        "timezone": "32400",
    }

    response = requests.get(COMMON_URL, headers=COMMON_HEADERS, params=params)

    if response.status_code == 200:
        return json.loads(response.text)['data']
    return None


def fetch_doc(cloudshop_id):
    cnt = 0
    while cnt < 20:
        try:
            doc = get_doc(cloudshop_id)
            return doc[0]
        except:
            cnt += 1
    raise Exception(f"Failed to fetch doc {cloudshop_id}")

    

def load_docs_from_text():
    print("Loading docs from text...")
    with open('data/inputs/cloudshop_ids.txt', 'r', encoding='utf-8') as f:
        cloudshop_ids = f.read().split('\n')
    raw_docs = []
    for cloudshop_id in cloudshop_ids:
        raw_docs.append({'_id': cloudshop_id})
    with open(f'data/raw/raw_docs.json', 'w', encoding='utf-8') as f:
        json.dump(raw_docs, f, ensure_ascii=False)


def load_docs_from_server_without_jump(id):
    print("Loading docs from server...")
    offset = id*5000
    params = {
        "path": f"/search/docs2/57c09c3b3ce7d59d048b46c9/{offset}/5000",
        "api": "v3",
        "timezone": "32400",
    }
    loaded_docs = []
    payload = {
        "start": 1451574000,
        "end":  1709823599,
    }
    response = requests.post(COMMON_URL, json=payload, params=params, headers=COMMON_HEADERS)
    if response.status_code == 200:
        print(f"{id} ---- SUCCESS")
        data = json.loads(response.text)['data']
        loaded_docs.extend(data)
    else:
        print("Request failed with status code:", response.status_code)

    loaded_docs = sorted(loaded_docs, key=lambda x: x['date'])
    loaded_docs = [{'_id': doc['_id']} for doc in loaded_docs]
    with open(f'data/raw/raw_docs_{id}.json', 'w', encoding='utf-8') as f:
        json.dump(loaded_docs, f, ensure_ascii=False)
    return 1




def load_docs_from_server(from_date, to_date, id):
    print("Loading docs from server...")
    params = {
        "path": "/search/docs2/57c09c3b3ce7d59d048b46c9/0/100000",
        "api": "v3",
        "timezone": "32400",
    }

    start_date = from_date
    delta = dt.timedelta(days=20)

    loaded_docs = []

    while start_date < to_date:
        end_date = min(start_date + delta, to_date)
        payload = {
            "start": int(start_date.timestamp()),
            "end": int(end_date.timestamp()),
            # "type": "purchases",
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

    with open(f'data/raw/raw_docs_{id}.json', 'w', encoding='utf-8') as f:
        json.dump(loaded_docs, f, ensure_ascii=False)
    return 1

def parallel_complete_docs(id):
    # Load raw documents
    with open(f'data/raw/raw_docs_{id}.json', 'r', encoding='utf-8') as f:
        loaded_docs = json.load(f)

    # Load already completed documents and exclude them from processing
    # already_completed = set()
    # completed_file_path = f'data/completed/completed_docs_{id}.json'
    # if os.path.exists(completed_file_path):
    #     with open(completed_file_path, 'r', encoding='utf-8') as f:
    #         already_completed_docs = json.load(f)
    #         already_completed = {doc['_id'] for doc in already_completed_docs}
    #         already_completed_docs.clear()
    # remaining_docs = [doc['_id'] for doc in loaded_docs if doc['_id'] not in already_completed]
    # print(f"Out of {len(loaded_docs)} docs,\n {len(already_completed)} docs are completed. {len(remaining_docs)} are remaining")
    
    # Fetch the remaining documents in parallel
    remaining_docs = [doc['_id'] for doc in loaded_docs]
    completed_docs = []
    completed_count = 0
    file_no = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        future_to_cloudshop_id = {executor.submit(fetch_doc, doc_id): doc_id for doc_id in remaining_docs}
        for future in concurrent.futures.as_completed(future_to_cloudshop_id):
            cloudshop_id = future_to_cloudshop_id[future]
            try:
                doc = future.result()
                completed_docs.append(doc)
                completed_count += 1
                if completed_count % 1000 == 0:
                    print(f"{completed_count} completed")
                    with open(f'data/completed/completed_docs_{id}_{file_no}.json', 'w', encoding='utf-8') as f:
                        json.dump(completed_docs, f, ensure_ascii=False)
                    file_no += 1
                    completed_docs = []
            except Exception as exc:
                print(f"Document {cloudshop_id} failed to fetch with exception: {exc}")


    # Combine all the files and save
    for i in range(file_no):
        with open(f'data/completed/completed_docs_{id}_{i}.json', 'r', encoding='utf-8') as f:
            completed_docs.extend(json.load(f))
        os.remove(f'data/completed/completed_docs_{id}_{i}.json')

    completed_docs = sorted(completed_docs, key=lambda x: x['date'])
    print(f"Saving {len(completed_docs)} completed docs")
    with open(f'data/completed/completed_docs_{id}.json', 'w', encoding='utf-8') as f:
        json.dump(completed_docs, f, ensure_ascii=False)
    return 1

def complete_docs(id):
    with open(f'data/raw/raw_docs_{id}.json', 'r', encoding='utf-8') as f:
        loaded_docs = json.load(f)
    completed_docs = []
    from_index = 0
    to_index = len(loaded_docs)
    print(from_index, to_index)
    file_no = 0
    for i, doc in enumerate(loaded_docs[from_index:to_index]):
        cloudshop_id = doc['_id']
        doc = fetch_doc(cloudshop_id)
        completed_docs.append(doc)
        if i%1000 == 500:
            with open(f'data/completed/completed_docs_{id}_{file_no}.json', 'w', encoding='utf-8') as f:
                json.dump(completed_docs, f, ensure_ascii=False)
            file_no += 1
            completed_docs = []
    for i in range(file_no):
        with open(f'data/completed/completed_docs_{id}_{i}.json', 'r', encoding='utf-8') as f:
            completed_docs.extend(json.load(f))
        # delete the file
        os.remove(f'data/completed/completed_docs_{id}_{i}.json')
    completed_docs = sorted(completed_docs, key=lambda x: x['date'])
    with open(f'data/completed/completed_docs_{id}.json', 'w', encoding='utf-8') as f:
        json.dump(completed_docs, f, ensure_ascii=False)
    return 1


def clean_docs(id):
    with open(f'data/completed/completed_docs_{id}.json', 'r', encoding='utf-8') as f:
        completed_docs = json.load(f)
    # response_data = read_json('data/raw/raw_docs.json')

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
            doc['bonus_cashback'] = thing.get('bonus_cashback', None)
            doc['status'] = thing['status']
            comment = thing.get('comment', '')
            if not comment:
                comment = ''

            doc['comment'] = comment
            if '111' in comment:
                doc['kkm'] = True
            else:
                doc['kkm'] = False
            doc['consultant'] = get_consultant(doc)

            cleaned_docs.append(doc)
            cnt += 1
    # sort cleaned docs by date
    cleaned_docs = sorted(cleaned_docs, key=lambda x: x['date'])
    with open(f"data/clean/clean_docs_{id}.json", 'w', encoding='utf-8') as f:
        json.dump(cleaned_docs, f, ensure_ascii=False)

    print(f"{cnt} scrapped successfully")
    return 1, stats


def dump_docs(id, base_url=BASE_URL):
    with open(f"data/clean/clean_docs_{id}.json", 'r', encoding='utf-8') as f:
        cleaned_docs = json.load(f)
    # sort cleaned_docs by date
    cleaned_docs = sorted(cleaned_docs, key=lambda x: x['date'])
    print(f"Total {len(cleaned_docs)} docs")
    docs_api = f'{base_url}/docs/api/mass-create-update'

    created_count = 0
    updated_count = 0
    error_count = 0
    docs_data = []
    for i, doc in enumerate(cleaned_docs):
        docs_data.append(doc)
        if i % 20 == 19:
            try:
                response = requests.post(docs_api, json=docs_data)
                statuses = response.json()['statuses']
                for stats in statuses:
                    if stats['action'] == 'create':
                        created_count += 1
                    elif stats['action'] == 'update':
                        updated_count += 1
                    else:
                        error_count += 1
                    # print(stats)
                docs_data = []
            except Exception as e:
                print("Failed to dump docs", response.status_code, response.json(), e)
                import sys
                print(sys.exc_info())
                sys.exit()
        if i%500 == 0:
            print(f"{i} docs processed")
    if len(docs_data) > 0:
        response = requests.post(docs_api, json=docs_data)
        try:
            statuses = response.json()['statuses']
            for stats in statuses:
                if stats['action'] == 'create':
                    created_count += 1
                elif stats['action'] == 'update':
                    updated_count += 1
                else:
                    error_count += 1
            docs_data = []
        except:
            print(response.status_code, response.json())
    stats = {
        "Total": updated_count + created_count,
        "Created Count": created_count,
        "Updated Count": updated_count,
        "Error Count": error_count,
    }
    return (1, stats)


def scrape_docs(skip_load, from_date, to_date, id=0):
    print("================ DOCS ================")

    ###### LOADING DOCS #######
    if not skip_load:
        status = 1
        # status = load_docs_from_server_without_jump(id)
        status = load_docs_from_server(from_date, to_date, id)
        if status == 0:
            print("Failed to load docs")
            return 0
        else:
            print("1) Loaded...")

        ###### COMPLETING DOCS #######
        # In the first step, positions are not provided (docs are incomplete). This step gets all docs with positions
        status = 1
        status = parallel_complete_docs(id)
        if status == 0:
            print("Failed to complete docs")
            return 0
        else:
            print("2) Completed...")
    ###### CLEANING DOCS #######
    status = 1
    status, stats = clean_docs(id)
    if status == 0:
        print("Failed to clean docs")
    else:
        print("3) Cleaned...")

    print(f"Results from {from_date} to {to_date}")
    print(stats)
    #### DUMPING DOCS #######
    status = 1
    # status, stats = dump_belepen_docs()
    status, stats = dump_docs(id, base_url=BASE_URL)
    if status == 0:
        print("Failed to dump docs")
    else:
        print("4) Dumped...")
        print(stats)


def dump_docs_only(id):
    # DUMPING DOCS #######
    status = 1
    # status, stats = dump_belepen_docs()
    status, stats = dump_docs(id)
    if status == 0:
        print("Failed to dump docs")
    else:
        print("4) Dumped...")
        print(stats)



if __name__ == '__main__':
    scrape_docs(dt.datetime.now() - dt.timedelta(hours=24), dt.datetime.now())