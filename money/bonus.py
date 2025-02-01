import json
import requests
import datetime as dt
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL
from utils.common import calculate_time


def load_bonuses_from_server(from_date, to_date):
    print("Loading bonuses from server...")
    params = {
        "path": "/bonus/57c09c3b3ce7d59d048b46c9/0/100000",
        "api": "v3",
        "timezone": "21600",
    }
    start_date = from_date
    delta = dt.timedelta(days=100)

    loaded_bonuses = []

    while start_date < to_date:
        end_date = min(start_date + delta, to_date)
        payload = {
            "start": int(start_date.timestamp()),
            "end": int(end_date.timestamp()),
        }
        response = requests.post(
            COMMON_URL, json=payload, params=params, headers=COMMON_HEADERS)
        if response.status_code == 200:
            print(f"{start_date} --- {end_date} --- SUCCESS")
            # print(response.text)
            data = json.loads(response.text)['data']
            loaded_bonuses.extend(data)
        else:
            print(f"{start_date} --- {end_date} --- FAILED")
        start_date += delta

    with open(f'data/raw/raw_bonuses.json', 'w', encoding='utf-8') as f:
        json.dump(loaded_bonuses, f, ensure_ascii=False)
    return 1


def get_bonus(cloudshop_id):
    params = {
        "path": f"/bonus/57c09c3b3ce7d59d048b46c9/{cloudshop_id}",
        "api": "v3",
        "timezone": "32400",
    }

    response = requests.get(COMMON_URL, headers=COMMON_HEADERS, params=params)

    if response.status_code == 200:
        return json.loads(response.text)['data']
    else:
        print("Request failed with status code:", response.status_code)


def complete_bonuses():
    with open(f'data/raw/raw_bonuses.json', 'r', encoding='utf-8') as f:
        loaded_bonuses = json.load(f)
    complete_bonuses = []
    from_index = 0
    to_index = len(loaded_bonuses)
    print(from_index, to_index)
    for i, bonus in enumerate(loaded_bonuses[from_index:to_index]):
        print(f"Completing bonus {i+1} of {to_index}")
        cloudshop_id = bonus['_id']
        got = False
        while not got:
            try:
                bonus = get_bonus(cloudshop_id)
                if bonus is None:
                    continue
                complete_bonuses.append(bonus)
                print(f'{i} of {to_index-from_index} completed, {cloudshop_id}')
                got = True
            except Exception as e:
                print(f"Failed to get bonus {cloudshop_id}, exception: {e}")
                pass
    with open(f'data/raw/completed_bonuses.json', 'w', encoding='utf-8') as f:
        json.dump(complete_bonuses, f, ensure_ascii=False)
    return 1


def handle_bonuses(thing):
    thing['closed'] = thing['closed'] if thing['closed'] else thing['open'] + 86400
    try:
        bonus =  {
            'cloudshop_id': thing['_id'],
            'register_id': thing['_register'],
            'store_id': thing['_store'],
            'number': thing['number'],

            'open': calculate_time(thing['open']),
            'closed': calculate_time(thing['closed']),
            'created': calculate_time(thing['created']),
            'updated': calculate_time(thing['updated']),
        }
        bonus['open_money'] = thing['data']['open_money']
        try:
            bonus['close_money'] = thing['data']['close_money']
        except:
            bonus['close_money'] = 0
        try:
            for item in thing['docs']:
                if item['type'] == 'sales':
                    bonus['sales_quantity'] = item['count']
                    bonus['sales_sum'] = item['sum']
                    bonus['sales_discount'] = item['discount_sum']
                if item['type'] == 'return_sales':
                    bonus['return_sales_quantity'] = item['count']
                    bonus['return_sales_sum'] = item['sum']
                    bonus['return_sales_discount'] = item['discount_sum']
        except:
            bonus['sales_quantity'] = 0
            bonus['sales_sum'] = 0
            bonus['sales_discount'] = 0
            bonus['return_sales_quantity'] = 0
            bonus['return_sales_sum'] = 0
            bonus['return_sales_discount'] = 0
        return bonus
    except Exception as e:
        print(e)


def clean_bonuses():
    with open(f'data/raw/completed_bonuses.json', 'r', encoding='utf-8') as f:
        completed_bonuses = json.load(f)
    cleaned_bonuses = []

    for thing in completed_bonuses:
        bonus = handle_bonuses(thing)
        if bonus:
            cleaned_bonuses.append(bonus)

    cleaned_bonuses = sorted(cleaned_bonuses, key=lambda x: x['open'])
    with open(f'data/clean/clean_bonuses.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_bonuses, f, ensure_ascii=False)
    return 1


def dump_bonuses():
    bonuses_api = f'{BASE_URL}/import/bonuses-api'
    with open(f"data/clean/clean_bonuses.json", 'r', encoding='utf-8') as f:
        cleaned_bonuses = json.load(f)
    temp = []
    cnt = 0
    total = 0
    created_count = 0
    updated_count = 0
    for bonus in cleaned_bonuses:
        temp.append(bonus)
        cnt += 1
        if cnt % 100 == 0:
            request_data = {
                'data': temp,
            }
            response = requests.post(bonuses_api, json=request_data).json()
            print(response)
            # if response['created_count'] == 0:
            #     break
            # total += response['total']
            # created_count += response['created_count']
            # updated_count += response['updated_count']
            temp = []
    request_data = {
        'data': temp,
    }
    response = requests.post(bonuses_api, json=request_data).json()
    print(response)
    return 1


def scrape_bonuses(skip_load, from_date, to_date):
    print("=================== SCRAPING SHIFTS STARTED ==============")
    if not skip_load:
        ##### LOAD SHIFTS #####
        status = 0
        status = load_bonuses_from_server(from_date, to_date)
        if status == 0:
            print("Loading bonuses from server failed")
        else:
            print("Loading bonuses from server finished")

        ##### COMPLETING SHIFTS #####
        status = 0
        status = complete_bonuses()
        if status == 0:
            print("Completing bonuses failed")
        else:
            print("Completing bonuses finished")

        print("=================== SCRAPING SHIFTS FINISHED ============== ")

    ##### CLEANING SHIFTS #####
    status = 0
    status = clean_bonuses()
    if status == 0:
        print("Cleaning bonuses failed")
    else:
        print("Cleaning bonuses finished")

    ### DUMPING SHIFTS #####
    status = 0
    status = dump_bonuses()
    if status == 0:
        print("Dumping bonuses failed")
    else:
        print("Dumping bonuses finished")
