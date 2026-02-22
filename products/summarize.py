import json
import pandas as pd
from pathlib import Path


def read_raw_products(file_path: str = None) -> list:
    """Read raw products from JSON file."""
    if file_path is None:
        file_path = Path(__file__).parent.parent / "data" / "raw" / "raw_products.json"
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Handle both direct list and wrapped response format
    if isinstance(data, dict) and "data" in data:
        return data["data"]
    return data


def products_to_excel(input_path: str = None, output_path: str = None):
    """
    Read raw_products.json and write essential product info to Excel.
    
    Columns: cloudshop_id, name, barcode, price, purchase, discount, cost, qty_current
    """
    products = read_raw_products(input_path)
    
    if not products:
        print("No products found!")
        return
    
    # Build rows for DataFrame
    rows = []
    for product in products:
        stock = product.get("stock", {})
        total_stock = product.get("total_stock", 0)
        
        # Calculate total if not provided
        if not total_stock and isinstance(stock, dict):
            total_stock = sum(stock.values())
        
        row = {
            "cloudshop_id": product.get("_id", ""),
            "name": product.get("name", ""),
            "barcode": product.get("barcode", ""),
            "price": product.get("price", 0),
            "purchase": product.get("purchase", 0),
            "discount": product.get("discount", 0),
            "cost": product.get("cost", 0),
            "qty_current": total_stock,
        }
        rows.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(rows)
    
    # Set output path
    if output_path is None:
        output_path = Path(__file__).parent.parent / "data" / "current_stock.xlsx"
    
    # Write to Excel
    df.to_excel(output_path, index=False, engine="openpyxl")
    print(f"Successfully exported {len(df)} products to {output_path}")
    
    return df


if __name__ == "__main__":
    products_to_excel()