import json
import datetime as dt


def write_to_json(data, location):
    try:
        with open(f'{location}', 'w', encoding='utf-8') as f:
            f.write(data)
    except:
        with open(f'{location}', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)


def read_json(location):
    with open(f'{location}', 'r', encoding='utf-8') as f:
        return json.load(f)


def calculate_time(timestamp):
    if timestamp is None:
        return None
    timestamp = dt.datetime.fromtimestamp(timestamp)
    return f"{timestamp}"
