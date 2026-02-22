# from numpy._core.multiarray import _ReturnType
from parties.suppliers import scrape_suppliers
from parties.clients import scrape_clients
from products.products import scrape_products
from company.registers import scrape_registers
from company.stores import scrape_stores
from company.shifts import scrape_shifts
from snaps.snaps import scrape_snaps
from money.bonus import scrape_bonus
from docs.docs import scrape_docs
from utils.config import SERVER_MODE, URLS
from sync.main import main as sync_notifications
import datetime as dt
import traceback
import argparse
import time

def main(skip_load, use_notifications=False):
    choosen_url = URLS[SERVER_MODE]
    # scrape_clients(skip_load, choosen_url)
    # print("Starting scrapers...")

    # try:
    # from_date = dt.datetime(2025, 4, 9, 0, 0, 0)
    # while dt.datetime.now() < dt.datetime.now().replace(hour=12, minute=30, second=0, microsecond=0):
    #     sleep = dt.datetime.now().replace(hour=12, minute=30, second=0, microsecond=0) - dt.datetime.now()
    #     print(f"Sleeping until 9:00 am... ({sleep})")
    #     time.sleep(abs(sleep.total_seconds()))
    # scrape_stores()
    # scrape_registers()
    # scrape_suppliers()

# try:
    # Use notification-based sync if requested
    if use_notifications:
        print("Using notification-based incremental sync...")
        stats = sync_notifications(limit=10000)
        print(f"Sync stats: {stats}")
        return
    
    # Legacy bulk sync approach
    from_date = dt.datetime(2026, 2, 20)
    to_date = dt.datetime.now()
    

    
# 
    # scrape_shifts(skip_load, from_date, to_date)  
    # scrape_products(skip_load, create_break=False) 
    
    scrape_clients(skip_load, create_break=False)   
    scrape_suppliers()
    scrape_docs(skip_load, from_date, to_date)
    scrape_bonus(skip_load, from_date, to_date)
    scrape_snaps(from_date, to_date, skip_load)
    return
    cnt = -1

    while True: 
        if cnt % 50 == 0:
            scrape_clients(skip_load, create_break=False)   
        else:
            scrape_clients(skip_load, create_break=True)
        scrape_docs(skip_load, from_date, to_date)
        # scrape_bonus(skip_load, from_date, to_date)
        # time.sleep(300)  
        from_date = to_date - dt.timedelta(hours=3)
        to_date = dt.datetime.now() 
        cnt += 1
        


        from_date = to_date - dt.timedelta(hours=3)
            
                
        
    # except Exception as e:
    #     print(f"An error occurred, {e} restarting in 10 minutes...")
        # traceback.print_exc() 
        # sleeping for 30 minutes before restarting
        #  
        return
        main(skip_load)



    # except Exception as e:
    #     print(f"An error occurred, {e} restarting in 10 minutes...")
        # traceback.print_exc() 
        # sleeping for 30 minutes before restarting
        #  
        # return
        # time.sleep(600)
        # main(skip_load)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip_load', action='store_true', help='Skip the loading of scrapers')
    parser.add_argument('--notifications', action='store_true', help='Use notification-based incremental sync')
    parser.add_argument('--limit', type=int, default=10000, help='Max notifications to process (when using --notifications)')
    args = parser.parse_args()
    
    if args.notifications:
        # Use notification-based sync (recommended approach)
        print("Running notification-based incremental sync...")
        try:
            stats = sync_notifications(limit=args.limit)
            print(f"Sync completed successfully: {stats}")
        except Exception as e:
            print(f"Notification sync failed: {e}")
            traceback.print_exc()
    else:
        # Legacy bulk sync approach
        main(skip_load=args.skip_load, use_notifications=False)
