import json
from collections import defaultdict

# Function to find clients with the same phone number
def find_clients_with_same_phone(file_path):
    # Load the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        clients = json.load(file)

    # Dictionary to group clients by phone number
    phone_groups = defaultdict(list)

    # Group clients by phone number
    for client in clients:
        phone = client.get('phone', None)
        if phone:  # Exclude clients with phone == None or empty
            phone_groups[phone].append(client)

    # Print clients with the same phone number and their bonus balances
    for phone, grouped_clients in phone_groups.items():
        if len(grouped_clients) > 1:  # Only print if more than one client has the same phone number
            print(f"Phone: {phone}")
            for client in grouped_clients:
                print(f"  Client Name: {client['name']}, Bonus Balance: {client.get('bonus_balance', 0)}")
            print()

if __name__ == "__main__":
    # Path to the clean_clients.json file
    file_path = 'clean_clients.json'

    # Find and print clients with the same phone number
    find_clients_with_same_phone(file_path)
