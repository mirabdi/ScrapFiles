import requests
from parties.suppliers import scrape_suppliers
from parties.clients import scrape_clients
from products.products import scrape_products
from company.accounts import scrape_accounts
from company.registers import scrape_registers
from company.shifts import scrape_shifts
from company.stores import scrape_stores
from docs.docs import scrape_docs
from utils.config import BASE_URL
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




if __name__ == '__main__':
    # SERVER_MODE = int(input("SERVER MODE: "))
    print("Starting scrappers...")
    from_date = dt.datetime.now() - dt.timedelta(days=3)
    cnt = 0
    while True:
        # if dt.datetime.now().hour < 12:
        #     time.sleep(1000)
        #     cnt = 0
        #     continue
        cnt += 1
        to_date = dt.datetime.now()
        print(f"================ CYCLE #{cnt} ================")
        if cnt%10 == 1:
            scrape_clients()
            scrape_shifts(to_date - dt.timedelta(days=3), to_date)
            if cnt > 1:
                from_date = dt.datetime.now() - dt.timedelta(hours=1)
        if cnt % 100 == 1:
            scrape_suppliers()
            scrape_stores()
            scrape_registers()
            scrape_products()
            if cnt > 1:
                from_date = dt.datetime.now() - dt.timedelta(hours=10)

        print("Scraping docs...")
        scrape_docs(from_date, to_date)
        # try:
        #     send_sms()
        # except:
        #     pass
        from_date = to_date
        time.sleep(60)
