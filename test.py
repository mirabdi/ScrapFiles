from utils.config import COMMON_HEADERS, COMMON_URL
import requests

def delete_product(cloudshop_id):
    params = {
        "path": f"/data/57c09c3b3ce7d59d048b46c9/catalog/{cloudshop_id}",
        "api": "v3",
        "timezone": "32400",
    }
    response = requests.delete(COMMON_URL, headers=COMMON_HEADERS, params=params)

    if response.status_code == 200:
        print(f"Product {cloudshop_id} deleted successfully")
        print(response.json())
        return 1
    else:
        print(response.status_code, response.json())
        return 0
    
if __name__ == '__main__':
    delete_product("58487d653ce7d5680e8b4970")