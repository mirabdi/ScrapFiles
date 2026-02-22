import requests



import json
import pandas as pd
from datetime import datetime

def write_json_to_excel(data):
    # Parse JSON string to list of dictionaries
    messages = json.loads(data)
    
    # Create list to store processed data
    processed_data = []
    lst = set()
    
    for message in messages:
        # Convert timestamp to datetime
        date = datetime.fromtimestamp(message['timestamp'])
        
        # Extract phone number from chatId by removing '@c.us'
        phone = message['chatId'].replace('@c.us', '')
        
        # Get text from either textMessage or extendedTextMessage
        text = message.get('textMessage', '')
        if not text and 'extendedTextMessage' in message:
            text = message['extendedTextMessage'].get('text', '')
            
        processed_data.append({
            'date': date,
            'phone': phone,
            'text': text
        })
        lst.add(phone)

    # write to phones.txt as a list with []
    lst = list(lst)
    print(len(lst))
    with open('phones.txt', 'w') as f:
        f.write(str(lst))

    # Create DataFrame and save to Excel
    df = pd.DataFrame(processed_data)
    df.to_excel('messages.xlsx', index=False)


url = "https://7105.api.greenapi.com/waInstance7105217922/lastOutgoingMessages/e7827e8a1412487c9fa2af09263d05c41646b2d7fcf040c2a8?minutes=6000"


headers= {}

response = requests.request("GET", url, headers=headers)

write_json_to_excel(response.text.encode('utf8'))

