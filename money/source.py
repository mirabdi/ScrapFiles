import json
import requests
import datetime as dt
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL
from utils.common import write_to_json, read_json, calculate_time

def load_sources():
    print("Loading sources from server...")
    params = {
        "path": "/data/57c09c3b3ce7d59d048b46c9/sources/", 
        "api": "v3",
        "timezone": "32400",
    }
    
    response = requests.get(COMMON_URL, params=params, headers=COMMON_HEADERS)
    if response.status_code == 200:
        print("Sources loaded successfully.")
        sources_data = json.loads(response.text)['data']
        with open('data/raw/raw_sources.json', 'w', encoding='utf-8') as f:
            json.dump(sources_data, f, ensure_ascii=False)
        return 1
    else:
        print("Request failed with status code:", response.status_code)
        return 0


def clean_sources():
    loaded_sources = []
    with open('data/raw/raw_sources.json', 'r', encoding='utf-8') as f:
        loaded_sources = json.load(f)
    
    cleaned_sources = []
    
    for source in loaded_sources:
        try:
            number = source['id']
            style = source['type']
            if style == 'credit':
                style = 'outgoing'
            elif style == 'debit':
                style = 'incoming'
            name = source['title']
            cloudshop_id = source['_id']
            try:
                created = calculate_time(source['created'])
            except:
                created = None
            try:
                deleted = source['deleted']
            except:
                deleted = False
            cleaned_source = {
                'cloudshop_id': cloudshop_id,
                'style': style,
                'number': number,
                'name': name,
                'created': created,
                'deleted': deleted,
            }
            cleaned_sources.append(cleaned_source)
        except Exception as e:
            print(e)
            print(source)
            break
    
    with open('data/clean/clean_sources.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_sources, f, ensure_ascii=False)
    
    return 1



def dump_sources():
    with open('data/clean/clean_sources.json', 'r', encoding='utf-8') as f:
        cleaned_sources = json.load(f)
    
    sources_api = f'{BASE_URL}/import/sources-api'
    
    temp = []
    cnt = 0
    total = 0
    created_count = 0
    updated_count = 0
    
    for source in cleaned_sources:
        temp.append(source)
        cnt += 1
        
        if cnt % 100 == 0:
            request_data = {
                'data': temp,
            }
            response = requests.post(sources_api, json=request_data).json()
            
            if response['created_count'] == 0:
                break
            
            total += response['total']
            created_count += response['created_count']
            updated_count += response['updated_count']
            temp = []
    
    request_data = {
        'data': temp,
    }
    response = requests.post(sources_api, json=request_data).json()
    total += response['total']
    created_count += response['created_count']
    updated_count += response['updated_count']
    
    stats = {
        "Total": total,
        "Created Count": created_count,
        "Updated Count": updated_count
    }
    print(stats)
    return 1



def scrape_sources():
    print("=============== SOURCES ===============")
    
    ########### Loading sources
    status = load_sources()
    if status == 1:
        print("Loading sources completed successfully.")
    else:
        print("Loading sources failed.")
    
    ########### Cleaning sources
    status = clean_sources()
    if status == 1:
        print("Cleaning sources completed successfully.")
    else:
        print("Cleaning sources failed.")
    
    ########## Dumping sources
    status = dump_sources()
    if status == 1:
        print("Dumping sources completed successfully.")
    else:
        print("Dumping sources failed.")

if __name__ == "__main__":
    scrape_sources()
