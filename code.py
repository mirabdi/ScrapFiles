# kvant.py
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# ===================== CONFIG =====================

BASE_DIR = "kvant"          # root download folder
YEAR_START = 1980
YEAR_END = 2020             # inclusive
EDITION_START = 1
EDITION_END = 12
PAGE_START = 1
PAGE_END = 99               # 0001–0099
MAX_WORKERS = 16            # threads
TIMEOUT = 10                # seconds

# ==================================================

def download_image(url, save_path):
    """Download a single image if it exists."""
    if os.path.exists(save_path):
        return

    try:
        r = requests.get(url, timeout=TIMEOUT)
        if r.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(r.content)
        # ignore 404 and other errors silently
    except requests.RequestException:
        pass


def main():
    os.makedirs(BASE_DIR, exist_ok=True)
    tasks = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for year in range(YEAR_START, YEAR_END + 1):
            for edition in range(EDITION_START, EDITION_END + 1):
                folder = os.path.join(BASE_DIR, str(year), f"{edition:02d}")
                os.makedirs(folder, exist_ok=True)

                for page in range(PAGE_START, PAGE_END + 1):
                    page_str = f"{page:04d}"
                    url = (
                        f"https://www.kvant.digital/data/"
                        f"kvant_{year}_{edition}/jpg/{page_str}.jpg"
                    )
                    save_path = os.path.join(folder, f"{page_str}.jpg")
                    tasks.append(
                        executor.submit(download_image, url, save_path)
                    )

        for _ in as_completed(tasks):
            pass

    print("Download completed.")


if __name__ == "__main__":
    main()
