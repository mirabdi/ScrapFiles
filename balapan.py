from parties.suppliers import scrape_suppliers
from parties.clients import scrape_clients
from products.products import scrape_products
from company.registers import scrape_registers
from company.stores import scrape_stores
from company.shifts import scrape_shifts
from docs.docs import scrape_docs
from utils.config import SERVER_MODE, URLS
import datetime as dt
import traceback
import argparse
import time

def main(skip_load):
    choosen_url = URLS[SERVER_MODE]
    # scrape_clients(skip_load, choosen_url)
    # print("Starting scrapers...")

    # try:
    # from_date = dt.datetime(2025, 1, 30, 0, 0, 0)
    # from_date = dt.datetime.now() - dt.timedelta(hours=5)
    to_date = dt.datetime.now()
    from_date = to_date - dt.timedelta(hours=30)
    # to_date = dt.datetime(2024, 6, 3, 0, 0,)
    # from_date = to_date.replace(hour=0, minute=0, second=0, microsecond=0) 
    # while dt.datetime.now().minute < 30:
    #     sleep = dt.datetime.now().replace(hour=12, minute=30, second=0, microsecond=0) - dt.datetime.now()
    #     print(f"Sleeping until 9:00 am... ({sleep})")
    #     time.sleep(abs(sleep.total_seconds()))

    # scrape_stores()
    # scrape_registers()
    # scrape_suppliers()
    # scrape_products(skip_load, create_break=False)
    # scrape_shifts(skip_load, from_date, to_date)

    
    cnt = -2
    while True: 
        # to_date = dt.datetime.now() 
        cnt += 1
        if cnt%100 == 0:
            scrape_clients(skip_load, create_break=False)
        else:
            scrape_clients(skip_load, create_break=True)
        scrape_docs(skip_load, from_date, to_date)
        from_date = to_date - dt.timedelta(minutes=20)

    # except Exception as e:
    #     print(f"An error occurred, {e} restarting in 10 minutes...")
        # traceback.print_exc() 
        # sleeping for 30 minutes before restarting
        #  
        return
        time.sleep(600)
        main(skip_load)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip_load', action='store_true', help='Skip the loading of scrapers')
    args = parser.parse_args()
    
    main(skip_load=args.skip_load)
