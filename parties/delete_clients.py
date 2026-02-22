import json
import requests
import ast
import sys
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.common import write_to_json, read_json, calculate_time, clean_phone
from utils.config import COMMON_HEADERS, COMMON_URL, BASE_URL

MAX_RETRIES = 5
failed = []


def delete_client(id):
    params = {
        "path": f"/data/57c09c3b3ce7d59d048b46c9/clients/{id}",
        "api": "v3",
        "timezone": "32400",
    }
    response = requests.delete(
        url=COMMON_URL,
        headers=COMMON_HEADERS,
        params=params,
    )
    if response.status_code == 200 and response.json().get("status"):
        return True
    return False


def delete_client_with_retry(c_id):
    """Delete a single client with retries."""
    attempts = 0

    while attempts < MAX_RETRIES:
        attempts += 1

        try:
            success = delete_client(c_id)

            if success:
                print(f"[SUCCESS] Deleted client {c_id} after {attempts} attempts")
                return True
            else:
                print(f"[FAIL] Can't delete client {c_id}, retrying... (attempt {attempts})")
                time.sleep(1)

        except Exception as e:
            print(f"[ERROR] Client {c_id} error: {e}, retrying... (attempt {attempts})")
            time.sleep(1)

    # After MAX_RETRIES failed attempts:
    failed.append(c_id)
    print(f"[FAILED PERMANENTLY] {c_id} after {MAX_RETRIES} attempts")
    return False


def delete_clients_multithreaded(max_threads=10):
    # Read clients
    with open("clients_for_deletion.txt", "r") as file:
        text = file.read()

    clients = ast.literal_eval(text)
    print(f"Total clients to delete: {len(clients)}")

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(delete_client_with_retry, c_id) for c_id in clients]

        for future in as_completed(futures):
            _ = future.result()

    print("\n========== FAILED CLIENT IDs ==========")
    print(failed)
    print(f"Total failed: {len(failed)}")


if __name__ == "__main__":
    delete_clients_multithreaded(max_threads=20)
