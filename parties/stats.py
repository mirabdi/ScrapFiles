import pandas as pd
import json

def create_excel_from_json(json_path, excel_path):
    # Read the JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Load data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Specify the columns you want in the Excel file
    columns_to_include = [
        'cloudshop_id', 'name', 'gender', 'created',  
         'phone',  'loyalty_type', 
        'bonus_balance', 'bonus_spent', 'cashback_rate', 'birthday'
    ]
    
    # Filter the DataFrame to only include the desired columns
    df = df[columns_to_include]

    # Save the DataFrame to an Excel file
    df.to_excel(excel_path, index=False)

    print(f"Excel file saved to {excel_path}")

# Usage
create_excel_from_json("../data/clean/clean_clients.json", "clean_clients.xlsx")
