import json
import requests
import datetime as dt
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL
from utils.common import write_to_json, read_json, calculate_time


def load_money(from_date, to_date):
    print("Loading money from server...")
    params = {
        "path": "/search/money/57c09c3b3ce7d59d048b46c9/0/100000",
        "api": "v3",
        "timezone": "32400",
    }
    start_date = from_date
    delta = dt.timedelta(days=20)

    loaded_money = []

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
            data = json.loads(response.text)['data']
            loaded_money.extend(data)
        else:
            print("Request failed with status code:", response.status_code)
        start_date = end_date
        print(end_date)
    with open(f'data/raw/raw_money.json', 'w', encoding='utf-8') as f:
        json.dump(loaded_money, f, ensure_ascii=False)
    return 1



def clean_money():
    loaded_money = []
    with open(f'data/raw/raw_money.json', 'r', encoding='utf-8') as f:
        loaded_money = json.load(f)
    cleaned_money = []
    total_in_quantity = 0
    total_out_quantity = 0
    total_in_sum = 0
    total_out_sum = 0
    for money in loaded_money:
        try:
            cloudshop_id = money['_id']
            number = money['number']
            date = calculate_time(money['date'])
            sign = money['sign']
            sum = money['sum']
            if sign == -1:
                style = 'outgoing'
                total_out_quantity += 1
                total_out_sum += sum
            else:
                style = 'incoming'
                total_in_quantity += 1
                total_in_sum += sum
            comment = money.get('comment', '')
            cash = money.get('cash', None)
            status = money['status']
            source_id = money['source']
            from_account_id = money['store']
            doc_id = money.get('doc_id', None)
            user_id = money.get('_user', None)
            contragent_info = money.get('contragent', None)
            client_id = None
            supplier_id = None
            to_account_id = None
            if contragent_info:
                tpy = contragent_info['type']
                _id = contragent_info['_id']
                if tpy == 'clients':
                    client_id = _id
                elif tpy == 'suppliers':
                    supplier_id = _id
                else:
                    to_account_id = _id
            register_id = money.get('_register', None)
            shift_id = money.get('_shift', None)
            try:
                created = calculate_time(money['created'])
                updated = calculate_time(money['updated'])
            except:
                created = None
                updated = None
            response = {
                'style': style,
                'cloudshop_id': cloudshop_id,
                'number': number,
                'date': date,
                'comment': comment,
                'source_id': source_id,
                'cash': cash,
                'sum': sum,
                'status': status,
                'doc_id': doc_id,
                'user_id': user_id,
                'from_account_id': from_account_id,
                'to_account_id': to_account_id,
                'client_id': client_id,
                'supplier_id': supplier_id,
                'register_id': register_id,
                'shift_id': shift_id,
                'created': created,
                'updated': updated,
            }
            cleaned_money.append(response)
        except Exception as e:
            print(e)
            print(money)
            break

    with open(f'data/clean/clean_money.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_money, f, ensure_ascii=False)
    stats = {
        'total_in_quantity': total_in_quantity,
        'total_out_quantity': total_out_quantity,
        'total_in_sum': total_in_sum,
        'total_out_sum': total_out_sum,
    }
    print(stats)
    return 1



def dump_money():
    with open(f'data/clean/clean_money.json', 'r', encoding='utf-8') as f:
        cleaned_money = json.load(f)
    
    cleaned_money = sorted(cleaned_money, key=lambda x: x['date'])
    money_api = f'{BASE_URL}/import/money-api'

    temp = []
    cnt = 0
    total = 0
    created_count = 0
    updated_count = 0
    for money in cleaned_money:
        temp.append(money)
        cnt += 1
        if cnt % 100 == 0:
            request_data = {
                'data': temp,
            }
            response = requests.post(money_api, json=request_data).json()
            if response['created_count'] == 0:
                break
            total += response['total']
            created_count += response['created_count']
            updated_count += response['updated_count']
            temp = []
    request_data = {
        'data': temp,
    }
    response = requests.post(money_api, json=request_data).json()
    # print(response)
    total += response['total']
    created_count += response['created_count']
    updated_count += response['updated_count']
    stats = {
        "Total": total,
        "Created Count": created_count,
        "Updated Count": updated_count
    }
    print(stats)
    return 1


def scrape_money(from_date, to_date):
    print("=============== MONEY ===============")
    
    ########### Loading money
    # status = 1
    # status = load_money(from_date, to_date)
    # if status == 1:
    #     print("Scraping money completed successfully.")
    # else:
    #     print("Scraping money failed.")
    
    ########### Cleaning money
    status = 1
    status = clean_money()
    if status == 1:
        print("Cleaning money completed successfully.")
    else:
        print("Cleaning money failed.")

    # ########### Dumping money
    status = 1
    status = dump_money()
    if status == 1:
        print("Dumping money completed successfully.")
    else:
        print("Dumping money failed.")


