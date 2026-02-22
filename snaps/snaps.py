import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import json
import requests
from utils.common import calculate_time
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL
from company.stores import read_stores
import concurrent.futures
import datetime as dt
from concurrent.futures import ProcessPoolExecutor, as_completed
import logging


def load_movements(start_date, end_date, store):
    params = {
        "path": "/report/57c09c3b3ce7d59d048b46c9/statistic/movements",
        "api": "v3",
        "timezone": "32400",
    }
    payload = {
        "start":int(start_date.timestamp()),
        "end": int(end_date.timestamp()), 
        "store_id": store['cloudshop_id'], 
    }
    while True:
        try:
            response = requests.post(COMMON_URL, headers=COMMON_HEADERS, params=params, json=payload)
            if response.status_code != 200:
                print("Request failed with status code:", response.status_code)
                continue
            data = json.loads(response.text)['data']
            with open(f'data/raw/movements.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
            return data
        except Exception as e:
            print(f"Error loading movements, retrying...: {e}")
            continue

def load_products_stats(start_date, end_date, store):
    params = {
        "path": "/report/57c09c3b3ce7d59d048b46c9/sales/groups-products",
        "api": "v3",
        "timezone": "32400",
    }
    payload = {
        "start":int(start_date.timestamp()),
        "end": int(end_date.timestamp()), 
        "store_id": store['cloudshop_id'], 
        "no_group": True
    }
    while True:
        try:
            response = requests.post(COMMON_URL, headers=COMMON_HEADERS, params=params, json=payload)
            if response.status_code != 200:
                print("Request failed with status code:", response.status_code)
                continue
            data = json.loads(response.text)['data']
            with open(f'data/raw/product_stats.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
            return data
        except Exception as e:
            print(f"Error loading product stats, retrying...: {e}")
            continue

def merge_to_snaps(movements, stats, store=None, date=None):
    """
    Merge product movements and sales stats into Snap-compatible dicts.

    Args:
        movements (list): list of product movement entries from CloudShop
        stats (list): list of product stats (sales, cost, margin, etc.)
        store (dict): store object (must contain cloudshop_id)
        date (datetime.date): day of snapshot

    Returns:
        list[dict]: structured Snap-like data ready for upload
    """

    # Create lookup tables
    movements_dict = {}
    if movements:
        for m in movements:
            pid = m['_id']['_id']
            movements_dict[pid] = m

    stats_dict = {}
    if stats:
        for s in stats:
            pid = s['_id']
            stats_dict[pid] = s

    # Merge by product_id (union of both sources)
    all_product_ids = set(movements_dict.keys()) | set(stats_dict.keys())
    snaps = []

    for pid in all_product_ids:
        mov = movements_dict.get(pid, {})
        stat = stats_dict.get(pid, {})

        product_data = mov.get('_id', {}) or stat.get('product', {}) or {}
        product_name = product_data.get('name', 'Unknown Product')

        # Movement-based quantities
        qty_before = mov.get('qty_before', 0) or 0
        qty_after = mov.get('qty_after', 0) or 0
        movs = mov.get('movs', {}) or {}
        docs = mov.get('docs', {}) or {}

        qty_in = movs.get('in', 0) or 0
        qty_out = movs.get('out', 0) or 0

        # Sales-related (from stats)
        sales_count = stat.get('sales', 0) or 0
        sales_qty = stat.get('count', 0) or 0
        sales_sum = stat.get('revenue', 0) or 0
        sales_purchase = stat.get('cost', 0) 
        sales_profit = stat.get('profit', 0) or (sales_sum - sales_purchase)

        # Product pricing
        price = stat.get('revenue', 0) / stat.get('count', 1) if stat.get('count', 0) else 0
        cost = stat.get('cost', 0) / stat.get('count', 1) if stat.get('count', 0) else 0
        margin = stat.get('margin', 0)
        rent = stat.get('rent', 0)

        # Derived fields
        purchase_open = qty_before * cost
        sum_open = qty_before * price
        purchase_close = qty_after * cost
        sum_close = qty_after * price

        # Other document-based quantities
        purchases_qty = docs.get('purchases', 0) or 0
        return_sales_qty = docs.get('return_sales', 0) or 0
        return_purchases_qty = docs.get('return_purchases', 0) or 0
        movements_qty = docs.get('movements', 0) or 0
        changes_in_qty = docs.get('changes_in', 0) or 0
        changes_out_qty = docs.get('changes_out', 0) or 0

        snap = {
            "product_id": pid,                     # CloudShop product _id
            "store_id": store["cloudshop_id"],     # Store cloudshop_id
            "date": date.strftime("%Y-%m-%d"),     # DateField

            # Product info
            "price": price,
            "cost": cost,
            "margin": margin,

            # Opening & closing stock
            "qty_open": qty_before,
            "purchase_open": purchase_open,
            "sum_open": sum_open,
            "qty_close": qty_after,
            "purchase_close": purchase_close,
            "sum_close": sum_close,

            # Movement & sales summary
            "qty_in": qty_in,
            "qty_out": qty_out,


            "sales_count": sales_count,
            "sales_qty": sales_qty,
            "sales_sum": sales_sum,
            "sales_purchase": sales_purchase,
            "sales_profit": sales_profit,

            # Other docs
            "purchases_qty": purchases_qty,
            "return_sales_qty": return_sales_qty,
            "return_purchases_qty": return_purchases_qty,
            "movements_qty": movements_qty,
            "changes_out_qty": changes_out_qty,
            "changes_in_qty": changes_in_qty,

            # Optional turnover metric
            "turn": rent or 0,
        }
        

        snaps.append(snap)

    with open(f'{BASE_DIR}/data/clean/snaps.json', 'w', encoding='utf-8') as f:
        json.dump(snaps, f, ensure_ascii=False)
    return snaps


def dump_snaps(snaps):
    snaps_url = f'{BASE_URL}/import/snaps-api'
    request_data = {
        'data': snaps
    }
    response = requests.post(snaps_url, json=request_data).json()
    total = response.get('total', None)
    if total is not None:
        return response
    else:
        print(response)
        return None

def process_store_date(store, start_date, end_date, skip_load=False):
    """Work done per store/date."""
    file_path = f'{BASE_DIR}/data/snaps/{store["cloudshop_id"]}_{start_date:%Y%m%d}.json'

    # --- If local file exists, reuse it ---
    if skip_load and os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            snaps = json.load(f)
    else:
        print(f"Processing {store['name']} @ {start_date:%Y-%m-%d}")
        movements = load_movements(start_date, end_date, store)
        stats = load_products_stats(start_date, end_date, store)
        snaps = merge_to_snaps(movements, stats, store, date=start_date)

        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save local JSON
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(snaps, f, ensure_ascii=False)

    # --- Upload step ---
    if len(snaps) == 0:
        print(f"No snaps to upload for {store['name']} @ {start_date:%Y-%m-%d}")
        return store, start_date
    response = dump_snaps(snaps)
    if not response:
        raise Exception("Failed to upload snaps")

    return store, start_date

def scrape_snaps(from_date, to_date, skip_load=False, max_workers=10, error_log_path="scrape_errors.log"):
    # to_date = to_date - dt.timedelta(days=1)  
    # --- Setup logging ---
    logging.basicConfig(
        filename=error_log_path,
        level=logging.ERROR,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stores = read_stores()
    from_date = from_date.replace(hour=0, minute=0, second=0)
    to_date = to_date.replace(hour=0, minute=0, second=0)

    delta = dt.timedelta(days=1)
    tasks = []

    # Build all tasks (store, date range)
    start_date = from_date
    while start_date < to_date:
        end_date = min(start_date + delta, to_date)
        for store in stores:
            store_created = dt.datetime.fromisoformat(store['created'])
            if store_created > end_date:
                continue
            tasks.append((store, start_date, end_date))
        start_date = end_date


    # --- Run tasks in parallel ---
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_store_date, store, sdate, edate, skip_load): (store, sdate)
            for store, sdate, edate in tasks
        }

        for future in as_completed(futures):
            store, sdate = futures[future]
            try:
                future.result()
                print(f"✅ Finished {store['name']} @ {sdate:%Y-%m-%d}")
            except Exception as e:
                msg = f"{store['name']} @ {sdate:%Y-%m-%d} failed: {e}"
                logging.error(msg)
                print(f"❌ {msg}")

    print(f"\nAll tasks complete. Errors (if any) logged to: {error_log_path}")