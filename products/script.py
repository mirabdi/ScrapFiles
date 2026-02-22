import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import json
import requests
from collections import defaultdict
from datetime import datetime

import pandas as pd

from utils.common import calculate_time
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL
from company.stores import read_stores


def stats_by_categories():
    """
    Calculate stock levels on category level, store by store.
    Merges products by their first category (each product counted once).
    
    Returns dict with structure:
    {
        category_name: {
            store_id: {
                'stock': total_qty,
                'total_purchase': qty * purchase,
                'total_price': qty * (price after discount)
            },
            ...
            'totals': {
                'stock': total_qty_all_stores,
                'total_purchase': total_purchase_all_stores,
                'total_price': total_price_all_stores
            }
        }
    }
    """
    stores = read_stores()
    store_ids = [s['cloudshop_id'] for s in stores]
    store_names = {s['cloudshop_id']: s['name'] for s in stores}
    
    with open(f'{BASE_DIR}/data/raw/raw_products.json', 'r', encoding='utf-8') as f:
        response_data = json.load(f)
    data = response_data['data']
    
    # Initialize category stats
    # Structure: {category: {store_id: {'stock': 0, 'total_purchase': 0, 'total_price': 0}}}
    category_stats = defaultdict(lambda: defaultdict(lambda: {'stock': 0, 'total_purchase': 0.0, 'total_price': 0.0}))
    
    for product in data:
        # Get first category, or 'Uncategorized' if none
        categories = product.get('categories', [])
        if categories and len(categories) > 0:
            category = categories[0]
            # Handle case where category itself might be a list
            if isinstance(category, list):
                category = category[0] if category else 'Uncategorized'
        else:
            category = 'Uncategorized'
        
        # Ensure category is a string
        category = str(category) if category else 'Uncategorized'
        
        # Get pricing info
        purchase_price = product.get('purchase', 0) or 0
        price = product.get('price', 0) or 0
        discount = product.get('discount', 0) or 0
        
        # Calculate price after discount
        discounted_price = price * (1 - discount / 100)
        
        # Get stock by store (handle case where stock might be a list or None)
        stock = product.get('stock', {})
        if not isinstance(stock, dict):
            stock = {}
        
        for store_id in store_ids:
            qty = stock.get(store_id, 0) or 0
            if qty != 0:
                category_stats[category][store_id]['stock'] += qty
                category_stats[category][store_id]['total_purchase'] += qty * purchase_price
                category_stats[category][store_id]['total_price'] += qty * discounted_price
    
    # Calculate totals per category and format output
    result = {}
    for category, store_data in category_stats.items():
        result[category] = {'stores': {}, 'totals': {'stock': 0, 'total_purchase': 0.0, 'total_price': 0.0}}
        
        for store_id, stats in store_data.items():
            store_name = store_names.get(store_id, store_id)
            result[category]['stores'][store_name] = {
                'store_id': store_id,
                'stock': stats['stock'],
                'total_purchase': round(stats['total_purchase'], 2),
                'total_price': round(stats['total_price'], 2)
            }
            result[category]['totals']['stock'] += stats['stock']
            result[category]['totals']['total_purchase'] += stats['total_purchase']
            result[category]['totals']['total_price'] += stats['total_price']
        
        result[category]['totals']['total_purchase'] = round(result[category]['totals']['total_purchase'], 2)
        result[category]['totals']['total_price'] = round(result[category]['totals']['total_price'], 2)
    
    # Sort by total stock descending
    result = dict(sorted(result.items(), key=lambda x: x[1]['totals']['stock'], reverse=True))
    
    # Save to Excel file
    date_str = datetime.now().strftime('%Y-%m-%d')
    excel_path = f'{BASE_DIR}/data/stats/category_stats_{date_str}.xlsx'
    
    # Save to JSON file
    with open(f'{BASE_DIR}/data/stats/category_stats_{date_str}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # Prepare data for Excel with MultiIndex columns (Store -> Metrics)
    # Get ordered store names
    store_order = [s['name'] for s in stores]
    
    # Build rows with category as index
    rows = []
    for category, cat_data in result.items():
        row = {'Category': category}
        for store_name in store_order:
            if store_name in cat_data['stores']:
                stats = cat_data['stores'][store_name]
                row[(store_name, 'Stock')] = stats['stock']
                row[(store_name, 'Purchase')] = stats['total_purchase']
                row[(store_name, 'Price')] = stats['total_price']
                row[(store_name, 'Margin')] = round(stats['total_price'] / stats['total_purchase'] - 1, 2)
            else:
                row[(store_name, 'Stock')] = 0
                row[(store_name, 'Purchase')] = 0.0
                row[(store_name, 'Price')] = 0.0
                row[(store_name, 'Margin')] = 0.0
        # Add totals
        row[('TOTAL', 'Stock')] = cat_data['totals']['stock']
        row[('TOTAL', 'Purchase')] = cat_data['totals']['total_purchase']
        row[('TOTAL', 'Price')] = cat_data['totals']['total_price']
        row[('TOTAL', 'Margin')] = round(cat_data['totals']['total_price'] - cat_data['totals']['total_purchase'], 2)
        rows.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(rows)
    df = df.set_index('Category')
    
    # Convert to MultiIndex columns
    tuples = [col for col in df.columns]
    df.columns = pd.MultiIndex.from_tuples(tuples, names=['Store', 'Metric'])
    
    # Sort by total stock descending
    df = df.sort_values(('TOTAL', 'Stock'), ascending=False)
    
    # Write to Excel
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Category Stats')
    
    print(f"\nExcel file saved: {excel_path}")
    
    # Print summary
    print(f"Processed {len(data)} products into {len(result)} categories")
    print(f"\nTop 10 categories by stock:")
    for i, (cat, stats) in enumerate(list(result.items())[:10]):
        print(f"  {i+1}. {cat}: {stats['totals']['stock']} units, "
              f"Purchase: {stats['totals']['total_purchase']:,.2f}, "
              f"Price: {stats['totals']['total_price']:,.2f}")
    
    return result


def get_store_products(store_id='667a67de8d522538ee0ba760'):
    with open(f'{BASE_DIR}/data/raw/raw_products.json', 'r', encoding='utf-8') as f:
        response_data = json.load(f)
    data = response_data['data']
    
    store_products = []
    for product in data:
        stock = product.get('stock', {})
        if not isinstance(stock, dict):
            stock = {}
        qty = stock.get(store_id, 0) or 0
        if qty > 0:
            store_products.append({'product': product['name'], 'quantity': qty})
    
    print(f"Store {store_id} has {len(store_products)} products in stock.")
    df = pd.DataFrame(store_products)
    df.to_excel(f'{BASE_DIR}/data/stats/store_{store_id}_products.xlsx', index=False)
    print(f"Excel file saved: {BASE_DIR}/data/stats/store_{store_id}_products.xlsx")
    return 


if __name__ == "__main__":
    # stats_by_categories()
    get_store_products('667a67de8d522538ee0ba760')  # Example store ID