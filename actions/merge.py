import json


def merge_clients():
    # Load the cleaned clients JSON data
    with open(f'clean_clients.json', 'r', encoding='utf-8') as f:
        cleaned_clients = json.load(f)
    
    # Dictionary to store merged clients by phone number
    merged_clients = {}
    
    for client in cleaned_clients:
        phone = client.get('phone')
        if not phone:
            continue
        
        if phone in merged_clients:
            # If the phone number already exists, merge the bonus balances and spent
            merged_clients[phone]['bonus_balance'] += client.get('bonus_balance', 0)
            merged_clients[phone]['bonus_spent'] += client.get('bonus_spent', 0)
        else:
            # Otherwise, add the client to the merged clients dictionary
            merged_clients[phone] = {
                'cloudshop_id': client['cloudshop_id'],
                'name': client['name'],
                'gender': client['gender'],
                'created': client['created'],
                'discount_percent': client.get('discount_percent'),
                'discount_card': client.get('discount_card'),
                'phone': client['phone'],
                'enable_savings': client.get('enable_savings'),
                'loyalty_type': client.get('loyalty_type'),
                'bonus_balance': client.get('bonus_balance', 0),
                'bonus_spent': client.get('bonus_spent', 0),
                'cashback_rate': client.get('cashback_rate'),
                'birthday': client.get('birthday')
            }

    # Convert the merged_clients dictionary back to a list
    merged_clients_list = list(merged_clients.values())

    # Save the merged clients data to a new file (optional)
    with open(f'merged_clients.json', 'w', encoding='utf-8') as f:
        json.dump(merged_clients_list, f, ensure_ascii=False, indent=4)

    return 1


if __name__ == "__main__":
    merge_clients()
