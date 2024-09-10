import datetime as dt
from dateutil.relativedelta import relativedelta
import json
import logging

from docs.docs import scrape_docs, dump_docs
from utils.config import SERVER_MODE, URLS

# Set up logging
logging.basicConfig(filename='scraping_logs.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

def main():
    logging.info("############ Starting scraping ############")
    start_date = dt.datetime(2017, 6, 1, 0, 0, 0)
    end_date = dt.datetime(2018, 1, 1, 0, 0, 0)
    # for id in range(68):
    #     try:
    #         with open(f'data/clean/clean_docs_{id}.json', 'r', encoding='utf-8') as f:
    #             clean_docs = json.load(f)
    #         if len(clean_docs) == 5000:
    #             logging.info(f"ID: {id}, docs already scraped for {id}")
    #         else:
    #             logging.warning(f"ID: {id}: Expected 5000 documents, found {len(clean_docs)}")
    #             scrape_docs(start_date, end_date, id)
    #         clean_docs = []
    #     except FileNotFoundError:
    #         logging.info(f"ID: {id}, FileNotFound, scraping docs for {id}...")
    #         scrape_docs(start_date, end_date, id)
    # logging.info("############ Scrapping completed ############")



    logging.info("############ Starting dumping to local ############")
    for id in range(68):
        try:
            with open(f'data/clean/clean_docs_{id}.json', 'r', encoding='utf-8') as f:
                clean_docs = json.load(f)
            status, stats = dump_docs(id=id, base_url="http://127.0.0.1:8000")
            logging.info(f"ID: {id}, {status}, {stats} dumped to local")
        except FileNotFoundError:
            logging.info(f"ID: {id}, FileNotFound")
            break
        except Exception as e:
            logging.error(f"ID: {id}, {e}")
            break
    logging.info("############ Dumping to local completed ############")





    # status, stats = dump_docs(id=3)
    logging.info("############ Starting dumping to server ############")
    for id in range(68) :
        try:
            with open(f'data/clean/clean_docs_{id}.json', 'r', encoding='utf-8') as f:
                clean_docs = json.load(f)
            status, stats = dump_docs(id=id, base_url="https://balapan.herokuapp.com")
            logging.info(f"ID: {id}, {status}, {stats} dumped to server")
        except FileNotFoundError:
            logging.info(f"ID: {id}, FileNotFound")
            break
        except Exception as e:
            logging.error(f"ID: {id}, {e}")
            break
    logging.info("############ Dumping to server completed ############")

if __name__ == "__main__":
    main()
