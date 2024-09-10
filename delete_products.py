import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import json
import requests
from utils.common import calculate_time
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL
import pandas as pd


def delete_products():
    params = {
        "path": "/data/57c09c3b3ce7d59d048b46c9/catalog/import",
        "api": "v3",
        "timezone": "32400",
    }
    payload = {}
    df = pd.read_excel('catalog.xlsx')
    cloudshop_ids = df['cloudshop_id'].tolist()
    print(len(cloudshop_ids))
    deletion = []
    cnt = 1
    for cloudshop_id in cloudshop_ids:
        if not pd.isna(cloudshop_id):
            deletion.append(cloudshop_id)
            if len(deletion) == 500:
                for i, cloudshop_id in enumerate(deletion):
                    payload[i] = {
                        "container": [],
                        "_id": cloudshop_id,
                        "deleted": True,
                    }
                response = requests.put(COMMON_URL, headers=COMMON_HEADERS, params=params, json=payload)
                if response.status_code == 200 and response.json()['status'] == True and response.json()['error'] == None:
                    print("deletion no", cnt)
                    # print(response.status_code, response.text)
                    cnt += 1
                    deletion = []
                else:
                    print("Request failed with status code:", response.status_code)
                    break
    if len(deletion) > 0:
        for i, cloudshop_id in enumerate(deletion):
            payload[i] = {
                "container": [],
                "_id": cloudshop_id,
                "delete": True,
            }
        response = requests.put(COMMON_URL, headers=COMMON_HEADERS, params=params, json=payload)
        if response.status_code == 200:
            print("deletion no", cnt)
            cnt += 1
            deletion = []
        else:
            print("Request failed with status code:", response.status_code)
            print(response.status_code, response.text)
    

if __name__ == "__main__":
    delete_products()
