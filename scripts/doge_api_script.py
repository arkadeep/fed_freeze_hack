import requests
import json
import csv
import sqlite3

URL_BASE = "https://api.doge.gov/savings/"
HEADERS = {
    "accept": "application/json"
}


PER_PAGE = 500

CONTRACT_SCHEMA = """
CREATE TABLE IF NOT EXISTS contracts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    piid TEXT,
    agency TEXT,
    vendor TEXT,
    value REAL,
    description TEXT,
    fpds_status TEXT,
    fpds_link TEXT,
    deleted_date TEXT,
    savings REAL
)
"""
GRANT_SCHEMA = """
CREATE TABLE IF NOT EXISTS grants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    agency TEXT,
    recipient TEXT,
    value REAL,
    savings REAL,
    link TEXT,
    description TEXT
)
"""
LEASE_SCHEMA = """
CREATE TABLE IF NOT EXISTS leases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    location TEXT,
    sq_ft INTEGER,
    description TEXT,
    value REAL,
    savings REAL,
    agency TEXT
)
"""

class SpendingItem:
    
    def __init__(self, name):
        self.name = name
        self.url = URL_BASE + self.name

    # Right now this returns all the items
    # In a future iteration, we should only fetch the items that have been updated
    # We can also return batches instead of all the items at once

    def fetch_all_items(self):
        all_data = []
        more_pages = True
        current_page = 1
        
        while more_pages:
            print(f"Fetching page {current_page}...")
            
            params = {
                "sort_by": "value",
                "sort_order": "asc",
                "page": current_page,
                "per_page": PER_PAGE
            }
            response = requests.get(self.url, params=params, headers=HEADERS)
            
            if response.status_code == 200:
                page_data = response.json()
                
                if 'result' in page_data and self.name in page_data['result']:
                    items = page_data['result'][self.name]
                else:
                    items = []
                    print("Warning: Could not find it in the response")
                
                if not items or (isinstance(items, list) and len(items) < PER_PAGE):
                    more_pages = False
                
                if items and isinstance(items, list):
                    all_data.extend(items)
                    print(f"Retrieved {len(items)} {self.name} from page {current_page}")
                else:
                    more_pages = False
                    print("No more data to retrieve or unexpected response format")
                current_page += 1
            else:
                print(f"Error: API request failed with status code {response.status_code}")
                print(response. text)
                more_pages = False

        all_data_tuples = [tuple(item.values()) for item in all_data]

        return all_data_tuples

    def save_to_csv(self, items):
        filename= "./data/" + self.name + "_all.csv"
        if not self.name:
            print("No data to save to CSV")
            return
    
        fieldnames = list(items[0].keys())
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(items)
        
        print(f"Data saved to {filename}")


class DatabaseUpdater:
    def __init__(self, name):
        self.db_name = name
        self.conn = sqlite3.connect(f'{self.db_name}.db')
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute(CONTRACT_SCHEMA)
        self.cursor.execute(GRANT_SCHEMA)
        self.cursor.execute(LEASE_SCHEMA)
        self.conn.commit()

    def save_to_db(self, batch_data, table_name):   
        try:
            if table_name == 'contracts':
                self.cursor.executemany('''
                INSERT INTO contracts (piid, agency, vendor, value, description, fpds_status, fpds_link, deleted_date, savings)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', batch_data)
            elif table_name == 'grants':
                self.cursor.executemany('''
                INSERT INTO grants (date, agency, recipient, value, savings, link, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', batch_data)        
            elif table_name == 'leases':
                self.cursor.executemany('''
                INSERT INTO leases (date, location, sq_ft, description, value, savings, agency)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', batch_data)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error saving data to {table_name}: {e}")
    
    def close_connection(self):
        self.conn.close()





db = DatabaseUpdater('./data/database/doge_api')
db.create_table()

contractsObject = SpendingItem('contracts')
all_items = contractsObject.fetch_all_items()
# contractsObject.save_to_csv(all_items)
db.save_to_db(all_items, 'contracts')

grantsObject = SpendingItem('grants')
all_items = grantsObject.fetch_all_items()
# grantsObject.save_to_csv(all_items)
db.save_to_db(all_items, 'grants')

leasesObject = SpendingItem('leases')
all_items = leasesObject.fetch_all_items()
# leasesObject.save_to_csv(all_items)
db.save_to_db(all_items, 'leases')

db.close_connection()