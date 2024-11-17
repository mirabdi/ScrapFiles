import json

# Function to calculate total bonus balance
def calculate_total_bonus_balance(file_path):
    # Load the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        clients = json.load(file)
    
    # Initialize the total bonus balance
    total_bonus_balance = 0
    total_bonus_spent = 0

    # Sum up the bonus balance for all clients
    for client in clients:
        bonus_balance = client.get('bonus_balance', 0) or 0  # Handle null values
        bonus_spent = client.get('bonus_spent', 0) or 0  # Handle null values
        total_bonus_balance += bonus_balance
        total_bonus_spent += bonus_spent


    return total_bonus_balance, total_bonus_spent

if __name__ == "__main__":
    # Path to the clean_clients.json file
    file_path = 'clean_clients.json'

    # Calculate total bonus balance
    total_bonus_balance, total_bonus_spent = calculate_total_bonus_balance(file_path)

    # Print the total bonus balance
    print(f"Total Bonus Balance: {total_bonus_balance}")
    print(f"Total Bonus Spent: {total_bonus_spent}")