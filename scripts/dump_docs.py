import json
import requests
import datetime as dt
# delay for 10 minutes
import time
print("Sleeping...")
# time.sleep(600)
# BASE_URL = "http://127.0.0.1:8000/"
BASE_URL = "https://balapan.herokuapp.com"
docs_api = f'{BASE_URL}/docs/api/mass-create-update'

with open('../data/clean/raw_docs.json', 'r', encoding='utf-8') as f:
    all_docs = json.load(f)

print(len(all_docs))
updated_count = 0
created_count = 0
docs_data = []
for i, doc in enumerate(all_docs):
    docs_data.append(doc)
    if i % 50 == 49:
        # print("Sending...")
        response = requests.post(docs_api, json=docs_data)
        print(f"Received with status code: {response.status_code}")
        try:
            statuses = response.json()['statuses']
            for stats in statuses:
                if stats['action'] == 'create':
                    created_count += 1
                elif stats['action'] == 'update':
                    updated_count += 1
                print(i, stats)
            docs_data = []
        except:
            print(i, response.status_code, response.json())
            break
response = requests.post(docs_api, json=docs_data)
try:
    statuses = response.json()['statuses']
    for stats in statuses:
        if stats['action'] == 'create':
            created_count += 1
        elif stats['action'] == 'update':
            updated_count += 1
        print(i, stats)
    docs_data = []
except:
    print(i, response.status_code, response.json())
stats = {
    "Total": updated_count + created_count,
    "Created Count": created_count,
    "Updated Count": updated_count
}
print(stats)
