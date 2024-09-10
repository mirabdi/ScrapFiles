from parties.suppliers import scrape_suppliers
from parties.clients import scrape_clients
from products.products import scrape_products
from docs.docs import scrape_docs
from utils.config import SERVER_MODE, BASE_URL
import datetime as dt
import time
import json
import requests


def send_sms():
    with open(f"data/clean/clean_docs.json", 'r', encoding='utf-8') as f:
        cleaned_docs = json.load(f)

    print(f"Sending SMS... {len(cleaned_docs)}")

    cleaned_docs = sorted(cleaned_docs, key=lambda x: x['date'])
    docs_api = f'{BASE_URL}/docs/api/send-sms'

    for i, doc in enumerate(cleaned_docs):
        try:
            response = requests.post(docs_api, json=doc)
            print(i, response.status_code, response.json())
        except Exception as e:
            print(i, e)


if __name__ == "__main__":
    from_date = dt.datetime.now() - dt.timedelta(hours=25)
    cnt = 0
    while True:
        cnt += 1
        to_date = dt.datetime.now()
        print(f"================ CYCLE #{cnt} ================")
        if cnt % 10 == 1:
            print("Scraping suppliers and clients...")
            scrape_suppliers()
            scrape_clients()
            if cnt % 30 == 1:
                print("Scraping products...")
                scrape_products()
            if cnt > 1:
                from_date = dt.datetime.now() - dt.timedelta(hours=2)
            continue

        print("Scraping docs...")
        scrape_docs(from_date, to_date)
        try:
            send_sms()
        except:
            pass
        # from_date = to_date
        print("Sleeping for 60 seconds ...")
        time.sleep(60)
