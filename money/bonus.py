import json
import requests
import os
import datetime as dt
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL
import concurrent.futures
import re
from utils.common import write_to_json, clean_phone, read_json, calculate_time

def load_bonus_from_server(from_date, to_date):
    print("Loading bonus from server...")
    params = {
        "path": "/search/bonus/57c09c3b3ce7d59d048b46c9/0/1000000",
        "api": "v3",
        "timezone": "32400",
    }

    start_date = from_date
    delta = dt.timedelta(days=30)

    loaded_bonus = []

    while start_date < to_date:
        end_date = min(start_date + delta, to_date)
        payload = {
            "start": int(start_date.timestamp()),
            "end": int(end_date.timestamp()),
        }
        while True:
            response = requests.post(
                COMMON_URL, json=payload, params=params, headers=COMMON_HEADERS)
            if response.status_code == 200:
                print(f"{start_date} --- {end_date} --- SUCCESS")
                data = json.loads(response.text)['data']
                loaded_bonus.extend(data)
                break
            else:
                print("Request failed with status code:", response.status_code, response.text)
        start_date = end_date
        print(end_date)
    loaded_bonus = sorted(loaded_bonus, key=lambda x: x.get("created", 0))
    with open(f'data/raw/bonus.json', 'w', encoding='utf-8') as f:
        json.dump(loaded_bonus, f, ensure_ascii=False)
    return 1


def clean_bonus():
    print("Cleaning bonus...")
    with open(f'data/raw/bonus.json', 'r', encoding='utf-8') as f:
        raw_bonus = json.load(f)

    cleaned_bonus = []
    for entry in raw_bonus:
        raw_amount = entry.get("amount", 0)
        try:
            amount = float(raw_amount)
            if amount.is_integer():
                amount = int(amount)
        except (TypeError, ValueError):
            amount = 0

        # Make amount negative for debit actions
        if entry.get("action") == "debit" and amount > 0:
            amount = -amount

        cleaned_entry = {
            "cloudshop_id": entry.get("_id"),
            "doc_id": entry.get("_doc"),
            "client_id": entry.get("_customer"),

            "amount": amount,
            "cashback_rate": entry.get("context", {}).get("cashback", 5),
            "balance_after": entry.get("remainder"),
            "balance_before": entry.get("context", {}).get("bonus_balance", 0),
            "spent_before": entry.get("context", {}).get("bonus_spent", 0),

            "style": entry.get("type"),
            "action": entry.get("action"),
            "comment": entry.get("comment"),

            "created_at": calculate_time(entry.get("created")),
            "updated_at": calculate_time(entry.get("updated")),
        }
        cleaned_bonus.append(cleaned_entry)

    print(f"Total bonus entries cleaned: {len(cleaned_bonus)}")
    with open(f'data/clean/bonus.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_bonus, f, ensure_ascii=False)
    return 1

def dump_bonus():
    with open(f'data/clean/bonus.json', 'r', encoding='utf-8') as f:
        cleaned_bonus = json.load(f)
    cleaned_bonus.sort(key=lambda x: x['created_at'])
    bonus_api = f"{BASE_URL}/import/bonus-api"
    total = 0
    created_count = 0
    updated_count = 0
    skipped_count = 0
    cnt = 0
    temp = []
    for bonus in cleaned_bonus:
        temp.append(bonus)
        cnt += 1
        if cnt % 500 == 0:
            response = requests.post(bonus_api, json={"data": temp})
            if response.status_code == 200:
                resp_data = response.json()
                created_count += resp_data.get("created_count", 0)
                updated_count += resp_data.get("updated_count", 0)
                skipped_count += resp_data.get("skipped_count", 0)
                total += len(temp)
                print(f"Dumped {total} bonus entries. Created: {created_count}, Updated: {updated_count}")
            else:
                print("Failed to dump bonus data:", response.status_code)
                return 0
            temp = []
    
    response = requests.post(bonus_api, json={"data": temp})
    if response.status_code == 200:
        resp_data = response.json()
        created_count += resp_data.get("created_count", 0)
        updated_count += resp_data.get("updated_count", 0)
        total += len(temp)
        print(f"Dumped {total} bonus entries. Created: {created_count}, Updated: {updated_count}")
    else:
        print("Failed to dump bonus data:", response.status_code)
        return 0
    stats = {
        "Total": total,
        "Created": created_count,
        "Updated": updated_count,
        "Skipped": skipped_count
    }
    print("Bonus dump stats:", stats)
    return 1


def scrape_bonus(skip_load, from_date, to_date):
    if not skip_load:
        status = 1
        status = load_bonus_from_server(from_date, to_date)
        if status == 0:
            print("Failed to load bonus from server.")
            return 0
        else:
            print("1) Successfully loaded bonus from server.")
    status = 1
    status = clean_bonus()
    if status == 0:
        print("Failed to clean bonus.")
        return 0
    else:
        print("2) Successfully cleaned bonus.")

    status = 1
    status = dump_bonus()
    if status == 0:
        print("Failed to dump bonus to DB.")
        return 0
    else:
        print("3) Successfully dumped bonus.")
    
    
    return 1