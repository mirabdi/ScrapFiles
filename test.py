from money.money import scrape_money
from money.source import scrape_sources
from company.accounts import scrape_accounts
from company.registers import scrape_registers
from company.shifts import scrape_shifts
from parties.clients import scrape_clients
from parties.suppliers import scrape_suppliers
from products.products import scrape_products
from notifications.notifications import scrape_notifications
from docs.docs import scrape_docs
from utils.config import SERVER_MODE
import datetime as dt

if __name__ == "__main__":
    from_date = dt.datetime(2024, 2, 1)
    to_date = dt.datetime(2024, 2, 2)
    # scrape_money(from_date, to_date)
    # scrape_clients()
    # scrape_suppliers()
    # scrape_products()
    # scrape_sources()
    # scrape_accounts()
    # scrape_registers()
    scrape_notifications(from_date, to_date)
    # scrape_shifts(from_date, to_date)
    # scrape_docs(from_date, to_date)
