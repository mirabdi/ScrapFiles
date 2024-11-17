import json
from collections import defaultdict

if __name__ == "__main__":
    print("Preparing data...")

    # Load the cleaned clients JSON data
    with open("clean_clients.json", "r", encoding="utf-8") as f:
        cleaned_clients = json.load(f)

    # Dictionary to store cloudshop_ids for each phone number
    phone_to_ids = defaultdict(list)

    # Populate the dictionary with phone numbers and corresponding cloudshop_ids
    for client in cleaned_clients:
        phone = client.get('phone')
        if phone:
            phone_to_ids[phone].append(client['cloudshop_id'])

    # Filter out phone numbers that appear more than once
    repeated_phones = {phone: ids for phone, ids in phone_to_ids.items() if len(ids) > 1}

    # Write the cloudshop_ids of clients with repeated phone numbers to a file
    with open("cloudshop_ids.txt", "w", encoding="utf-8") as f:
        if repeated_phones:
            for phone, ids in repeated_phones.items():
                # Write the cloudshop_ids for each repeated phone number on a new line
                f.write(", ".join(ids) + "\n")
            print(f"Written cloudshop_ids of clients with repeated phone numbers to 'cloudshop_ids.txt'.")
        else:
            print("No repeated phone numbers found.")
