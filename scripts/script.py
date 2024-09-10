import json
import requests
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL
import datetime as dt
import sys

# read by ignoring errors
with open(f"data/raw/raw_docs.json", 'r', encoding='utf-8') as f:
    raw_docs = json.load(f)
print(len(raw_docs))
cloudshop_ids = []
for i in raw_docs:
    cloudshop_ids.append(i['_id'])
docs_api = f'{BASE_URL}/docs/api/doc-check'

total = 0
created_count = 0
updated_count = 0
print(len(cloudshop_ids))
for i, cloudshop_id in enumerate(cloudshop_ids):
    doc = {
        "cloudshop_id": cloudshop_id,
        "action": "check"
    }
    response = requests.post(docs_api, json=doc)
    if response.json()['action'] == 'create':
        print(cloudshop_id)
        created_count += 1
    else:
        updated_count += 1
    if response.status_code != 200:
        break

    total += 1

stats = {
    "Total": total,
    "Created Count": created_count,
    "Updated Count": updated_count
}
