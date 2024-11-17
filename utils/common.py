import json
import datetime as dt


def write_to_json(data, location):
    try:
        with open(f'{location}', 'w', encoding='utf-8') as f:
            f.write(data)
    except:
        with open(f'{location}', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

def clean_phone(phone):
    phone_number = phone
    if phone_number is not None:
        phone_number = ''.join(filter(str.isdigit, phone_number))
        if len(phone_number) == 9:
            phone_number = '996'+phone_number
        elif len(phone_number) == 10 and phone_number[0] == '0':
            phone_number = '996'+phone_number[1:10]
        elif len(phone_number) != 12:
            phone_number = None
    return phone_number

def read_json(location):
    with open(f'{location}', 'r', encoding='utf-8') as f:
        return json.load(f)


def calculate_time(timestamp):
    if not timestamp:
        return None
    timestamp = dt.datetime.fromtimestamp(timestamp)
    return f"{timestamp}"
