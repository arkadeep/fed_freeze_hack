import requests
import json
import csv

URL_BASE = "https://api.doge.gov/savings/"
HEADERS = {
    "accept": "application/json"
}


PER_PAGE = 500



class SpendingItem:
    
    def __init__(self, name):
        self.name = name
        self.url = URL_BASE + self.name
        
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
        
        return all_data

    def save_to_csv(self, items):
        filename= "fed_freeze_hack/data/" + self.name + "_all.csv"
        if not self.name:
            print("No data to save to CSV")
            return
        
    
        fieldnames = list(items[0].keys())
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(items)
        
        print(f"Data saved to {filename}")



contractsObject = SpendingItem('contracts')
all_items = contractsObject.fetch_all_items()
contractsObject.save_to_csv(all_items)

grantsObject = SpendingItem('grants')
all_items = grantsObject.fetch_all_items()
grantsObject.save_to_csv(all_items)

leasesObject = SpendingItem('leases')
all_items = leasesObject.fetch_all_items()
leasesObject.save_to_csv(all_items)