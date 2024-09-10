import json
import requests
import datetime as dt
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL
from utils.common import calculate_time


def load_shifts_from_server(from_date, to_date):
    print("Loading shifts from server...")
    params = {
        "path": "/shift/57c09c3b3ce7d59d048b46c9/0/100000",
        "api": "v3",
        "timezone": "21600",
    }
    start_date = from_date
    delta = dt.timedelta(days=100)

    loaded_shifts = []

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
            loaded_shifts.extend(data)
        else:
            print(f"{start_date} --- {end_date} --- FAILED")
        start_date += delta

    with open(f'data/raw/raw_shifts.json', 'w', encoding='utf-8') as f:
        json.dump(loaded_shifts, f, ensure_ascii=False)
    return 1


def get_shift(cloudshop_id):
    params = {
        "path": f"/shift/57c09c3b3ce7d59d048b46c9/{cloudshop_id}",
        "api": "v3",
        "timezone": "32400",
    }

    response = requests.get(COMMON_URL, headers=COMMON_HEADERS, params=params)

    if response.status_code == 200:
        return json.loads(response.text)['data']
    else:
        print("Request failed with status code:", response.status_code)


def complete_shifts():
    with open(f'data/raw/raw_shifts.json', 'r', encoding='utf-8') as f:
        loaded_shifts = json.load(f)
    complete_shifts = []
    from_index = 0
    to_index = len(loaded_shifts)
    print(from_index, to_index)
    for i, shift in enumerate(loaded_shifts[from_index:to_index]):
        print(f"Completing shift {i+1} of {to_index}")
        cloudshop_id = shift['_id']
        got = False
        while not got:
            try:
                shift = get_shift(cloudshop_id)
                if shift is None:
                    continue
                complete_shifts.append(shift)
                print(f'{i} of {to_index-from_index} completed, {cloudshop_id}')
                got = True
            except Exception as e:
                print(f"Failed to get shift {cloudshop_id}, exception: {e}")
                pass
    with open(f'data/raw/completed_shifts.json', 'w', encoding='utf-8') as f:
        json.dump(complete_shifts, f, ensure_ascii=False)
    return 1


def handle_shifts(thing):
    thing['closed'] = thing['closed'] if thing['closed'] else thing['open'] + 86400
    try:
        shift =  {
            'cloudshop_id': thing['_id'],
            'register_id': thing['_register'],
            'store_id': thing['_store'],
            'number': thing['number'],

            'open': calculate_time(thing['open']),
            'closed': calculate_time(thing['closed']),
            'created': calculate_time(thing['created']),
            'updated': calculate_time(thing['updated']),
        }
        shift['open_money'] = thing['data']['open_money']
        try:
            shift['close_money'] = thing['data']['close_money']
        except:
            shift['close_money'] = 0
        try:
            for item in thing['docs']:
                if item['type'] == 'sales':
                    shift['sales_quantity'] = item['count']
                    shift['sales_sum'] = item['sum']
                    shift['sales_discount'] = item['discount_sum']
                if item['type'] == 'return_sales':
                    shift['return_sales_quantity'] = item['count']
                    shift['return_sales_sum'] = item['sum']
                    shift['return_sales_discount'] = item['discount_sum']
        except:
            shift['sales_quantity'] = 0
            shift['sales_sum'] = 0
            shift['sales_discount'] = 0
            shift['return_sales_quantity'] = 0
            shift['return_sales_sum'] = 0
            shift['return_sales_discount'] = 0
        return shift
    except Exception as e:
        print(e)


def clean_shifts():
    with open(f'data/raw/completed_shifts.json', 'r', encoding='utf-8') as f:
        completed_shifts = json.load(f)
    cleaned_shifts = []

    for thing in completed_shifts:
        shift = handle_shifts(thing)
        if shift:
            cleaned_shifts.append(shift)

    cleaned_shifts = sorted(cleaned_shifts, key=lambda x: x['open'])
    with open(f'data/clean/clean_shifts.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_shifts, f, ensure_ascii=False)
    return 1


def dump_shifts():
    shifts_api = f'{BASE_URL}/import/shifts-api'
    with open(f"data/clean/clean_shifts.json", 'r', encoding='utf-8') as f:
        cleaned_shifts = json.load(f)
    temp = []
    cnt = 0
    total = 0
    created_count = 0
    updated_count = 0
    for shift in cleaned_shifts:
        temp.append(shift)
        cnt += 1
        if cnt % 100 == 0:
            request_data = {
                'data': temp,
            }
            response = requests.post(shifts_api, json=request_data).json()
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
    response = requests.post(shifts_api, json=request_data).json()
    print(response)
    return 1


def scrape_shifts(skip_load, from_date, to_date):
    print("=================== SCRAPING SHIFTS STARTED ==============")
    if not skip_load:
        ##### LOAD SHIFTS #####
        status = 0
        status = load_shifts_from_server(from_date, to_date)
        if status == 0:
            print("Loading shifts from server failed")
        else:
            print("Loading shifts from server finished")

        ##### COMPLETING SHIFTS #####
        status = 0
        status = complete_shifts()
        if status == 0:
            print("Completing shifts failed")
        else:
            print("Completing shifts finished")

        print("=================== SCRAPING SHIFTS FINISHED ============== ")

    ##### CLEANING SHIFTS #####
    status = 0
    status = clean_shifts()
    if status == 0:
        print("Cleaning shifts failed")
    else:
        print("Cleaning shifts finished")

    ### DUMPING SHIFTS #####
    status = 0
    status = dump_shifts()
    if status == 0:
        print("Dumping shifts failed")
    else:
        print("Dumping shifts finished")
