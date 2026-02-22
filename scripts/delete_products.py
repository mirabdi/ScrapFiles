import ast
import requests
import sys, os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.common import calculate_time
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL


def delete_product(cloudshop_id):
    params = {
        "path": f"/data/57c09c3b3ce7d59d048b46c9/catalog/{cloudshop_id}",
        "api": "v3",
        "timezone": "32400",
    }

    try:
        response = requests.delete(COMMON_URL, headers=COMMON_HEADERS, params=params)
        if response.status_code == 200:
            return (cloudshop_id, True)
        else:
            return (cloudshop_id, False)
    except Exception as e:
        return (cloudshop_id, False)


def main():
    # Read product IDs
    with open("delete_products.txt", "r", encoding="utf-8") as f:
        # content = f.read()
        # ids = ast.literal_eval(content)
        ids = [line.strip() for line in f if line.strip()]

    print(len(ids), "ids loaded, proceeding to delete them")

    deleted_file = "deleted_products.txt"
    error_file = "error_products.txt"

    # Clear old logs
    open(deleted_file, "w").close()
    open(error_file, "w").close()

    # Run deletions in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(delete_product, id) for id in ids]

        for future in as_completed(futures):
            cloudshop_id, success = future.result()
            if success:
                with open(deleted_file, "a", encoding="utf-8") as df:
                    df.write(str(cloudshop_id) + "\n")
            else:
                with open(error_file, "a", encoding="utf-8") as ef:
                    ef.write(str(cloudshop_id) + "\n")
      


if __name__ == "__main__":
    main()
