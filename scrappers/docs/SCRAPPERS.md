# Scrappers Documentation

## Overview
This project consists of scrappers that fetch data from CloudShop APIs and push cleaned data to a Balapan backend. The main orchestrator is `balapan.py`, which coordinates individual domain scrappers (clients, products, shifts, docs, etc.) and controls execution windows.

## Entry Point: balapan.py
- Purpose: Orchestrates which scrappers run and in what order, controlling time windows for incremental runs.
- Key imports: `scrape_clients`, `scrape_products`, `scrape_registers`, `scrape_stores`, `scrape_shifts`, `scrape_bonus`, `scrape_docs`.
- Config: Chooses target base URL via `SERVER_MODE` and `URLS` from `utils/config.py`.
- CLI: Accepts a `--skip_load` flag to bypass the initial server fetch in scrappers that support it.

Code reference:
```1:18:c:\Users\abdir\Desktop\dev\ScrapFiles\scrappers\balapan.py
from parties.suppliers import scrape_suppliers
from parties.clients import scrape_clients
from products.products import scrape_products
from company.registers import scrape_registers
from company.stores import scrape_stores
from company.shifts import scrape_shifts
from money.bonus import scrape_bonus
from docs.docs import scrape_docs
from utils.config import SERVER_MODE, URLS
```

### Typical Orchestration Flow
- Define a moving time window `from_date` → `to_date`.
- Run time-bounded scrappers (e.g., shifts, docs), and unbounded reloads (e.g., products/clients) with `create_break` toggles for pacing.

Code reference:
```30:59:c:\Users\abdir\Desktop\dev\ScrapFiles\scrappers\balapan.py
try:
    from_date = dt.datetime(2025, 10, 27)
    to_date = dt.datetime.now()

    scrape_shifts(skip_load, from_date, to_date)
    scrape_products(skip_load, create_break=False)

    cnt = 0
    while True:
        if cnt % 50 == 0:
            scrape_clients(skip_load, create_break=False)
        else:
            scrape_clients(skip_load, create_break=True)
        scrape_docs(skip_load, from_date, to_date)
        to_date = dt.datetime.now()
        return
```

### Running the Orchestrator
```bash
python balapan.py --skip_load
```
- With `--skip_load`: scrappers that support it will skip fetching raw IDs from CloudShop and operate on previously saved inputs.
- Without `--skip_load`: scrappers will perform a fresh load step from CloudShop where implemented.

## Configuration
Located in `utils/config.py`.
- `URLS` / `SERVER_MODE`: selects target Balapan backend base URL.
- `BASE_URL`: resolved from `URLS[SERVER_MODE]`.
- `COMMON_URL` and `COMMON_HEADERS`: used to call CloudShop endpoints.

Code reference:
```5:18:c:\Users\abdir\Desktop\dev\ScrapFiles\scrappers\utils\config.py
URLS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002",
    "http://127.0.0.1:8003",
    "https://balapan.herokuapp.com",
    "http://172.30.1.44:8000",
    "http://192.168.0.103:8000",
    "https://cloudshop-855e74fca5e5.herokuapp.com"
]
SERVER_MODE = 4
BASE_URL = URLS[SERVER_MODE]
```

## Docs Scrapper (`docs/docs.py`)
The docs scrapper demonstrates the standard 4-phase pipeline used across scrappers that deal with time-bounded events:

1) Load raw document IDs from CloudShop for a time window.
2) Complete docs by fetching full payloads (positions, etc.).
3) Clean/transform docs into normalized objects.
4) Dump the cleaned docs in batches to the Balapan backend.

Top-level function:
```402:455:c:\Users\abdir\Desktop\dev\ScrapFiles\scrappers\docs\docs.py
def scrape_docs(skip_load, from_date, to_date, id=0, file_no=0, type=None):
    print("================ DOCS ================")

    ###### LOADING DOCS #######
    if not skip_load:
        status = load_docs_from_server(from_date, to_date, id, type)
        if status == 0:
            print("Failed to load docs")
            return 0
        else:
            print("1) Loaded...")

        ###### COMPLETING DOCS #######
        if file_no == 0:
            status = parallel_complete_docs(id)
            if status == 0:
                print("Failed to complete docs")
                return 0
            else:
                print("2) Completed...")
    if file_no != 0:
        status = combine_files(id, file_no)
        if status == 0:
            print("Failed to combine files")
            return 0
        else:
            print("2) Combined...")

    ###### CLEANING DOCS #######
    status, stats = clean_docs(id)
    if status == 0:
        print("Failed to clean docs")
    else:
        print("3) Cleaned...")

    print(f"Results from {from_date} to {to_date}")
    print(stats)

    #### DUMPING DOCS #######
    status, stats = dump_docs(id, base_url=BASE_URL)
    if status == 0:
        print("Failed to dump docs")
    else:
        print("4) Dumped...")
        print(stats)
```

### Pipeline internals (Docs)
- Load: `load_docs_from_server(from_date, to_date, id, type)` paginates across the time range, writing `data/raw/raw_docs_{id}.json`.
- Complete: `parallel_complete_docs(id)` fetches each document by `_id` concurrently and writes chunked `data/completed/*.json`, then merges into `data/completed/completed_docs_{id}.json`.
- Clean: `clean_docs(id)` normalizes documents, enriches with derived fields like consultant, flags (`kkm`), and counters, and writes `data/clean/clean_docs_{id}.json`.
- Dump: `dump_docs(id, base_url)` POSTs in batches of 10 to `{BASE_URL}/docs/api/mass-create-update` with create/update tracking.

## Adding a New Scrapper
- Create a module with a `scrape_<domain>(...)` function that follows the 4-phase pattern where applicable: load → complete → clean → dump.
- Accept `skip_load` to allow skipping CloudShop fetches when local raw inputs already exist.
- Write intermediate files into `data/raw`, `data/completed`, `data/clean` consistently.
- Batch outgoing writes to backend and guard for partial failures; keep counters for created/updated/errors.
- Integrate into `balapan.py` by importing your function and scheduling it in the main loop where appropriate.

## Usage Examples
- Run docs for last 24 hours from the module directly:
```470:471:c:\Users\abdir\Desktop\dev\ScrapFiles\scrappers\docs\docs.py
if __name__ == '__main__':
    scrape_docs(dt.datetime.now() - dt.timedelta(hours=24), dt.datetime.now())
```
- Orchestrated run (recommended):
```bash
python balapan.py --skip_load
```

## Operational Notes
- `COMMON_HEADERS` contains authentication/session cookies for CloudShop; ensure these are valid or injected from a secure source for production.
- `SERVER_MODE` controls target backend; confirm before running to avoid writing to unintended environments.
- Long runs: consider enabling delays between loops in `balapan.py` to control API pressure.

## Troubleshooting
- Empty outputs: verify time window and CloudShop credentials.
- High error counts on dump: log and inspect response bodies; confirm backend schema accepts the transformed docs.
- Missing `positions` in docs: ensure the Complete phase is executed (and not skipped by `skip_load`).
