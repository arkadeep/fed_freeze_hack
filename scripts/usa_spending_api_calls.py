import csv
from pathlib import Path
import requests
import json
import os

# Logic for consolidating DOGE data with USA Spending information
# Doing this allows us to get vendor information


FILE_PATH = "data/snippets/all_doge_contracts.csv"


# Base URL for USA Spending API
BASE_URL = "https://api.usaspending.gov/api/v2"


def search_by_piid(piid):
    """
    Search for awards within a specific time period
    """
    endpoint = f"{BASE_URL}/search/spending_by_award/"

    payload = {
        "subawards": False,
        "limit": 1,
        "page": 1,
        "filters": {
            "award_type_codes": ["A", "B", "C"],
            "award_ids": [f"{piid}"],
        },
        "fields": [
            "Award ID",
            "Recipient Name",
            "recipient_id",
            "Description",
            "Start Date",
            "End Date",
            "Award Amount",
            "Awarding Agency",
            "Awarding Sub Agency",
            "Contract Award Type",
            "Award Type",
            "Funding Agency",
            "Funding Sub Agency",
        ],
    }

    response = requests.post(endpoint, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def process_csv(file_path):
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            piid = row.get("piid", "").strip()
            if piid not in ["Unavailable for legal reason", "Charge Card Purchase"]:
                # Process the row as needed
                print(f"Processing row with PIID: {piid}")

                search_by_piid_result = search_by_piid(piid)
                if search_by_piid_result:
                    print(json.dumps(search_by_piid_result, indent=4))


# Example usage
process_csv(FILE_PATH)


# (whatsapp_rag) ➜  fed_freeze_hack git:(main) ✗ >....
#   -H "Content-Type: application/json" \
#   -d '{
#       "subawards": false,
#       "limit": 1,
#       "page": 1,
#       "filters": {
#             "award_type_codes": ["A", "B", "C"],
#             "award_ids": ["93310023P0021"]
#       },
#       "fields": [
#             "Description",
#             "Award ID",
#             "Recipient Name",
#             "Recipient DUNS Number",
#             "recipient_id",
#             "Start Date",
#             "End Date",
#             "Award Amount",
#             "Awarding Agency",
#             "Awarding Sub Agency",
#             "Contract Award Type",
#             "Award Type",
#             "Funding Agency",
#             "Funding Sub Agency"
#       ]
#   }'
# {"limit":1,"results":[{"internal_id":162790169,"Description":"EEO DEIA SUPPORT","Award ID":"93310023P0021","Recipient Name":"CORICHIA BRISCO ENTERPRISES LLC","Recipient DUNS Number":null,"recipient_id":"34228757-4b3c-8dac-90bb-a06834ec884a-C","Start Date":"2023-09-18","End Date":"2025-01-22","Award Amount":237518.75,"Awarding Agency":"Federal Mediation and Conciliation Service","Awarding Sub Agency":"Federal Mediation and Conciliation Service","Contract Award Type":"PURCHASE ORDER","Award Type":null,"Funding Agency":"Federal Mediation and Conciliation Service","Funding Sub Agency":"Federal Mediation and Conciliation Service","awarding_agency_id":1125,"agency_slug":"federal-mediation-and-conciliation-service","generated_internal_id":"CONT_AWD_93310023P0021_9300_-NONE-_-NONE-"}],"page_metadata":{"page":1,"hasNext":false,"last_record_unique_id":null,"last_record_sort_value":"None"},"messages":["For searches, time period start and end dates are currently limited to an earliest date of 2007-10-01.  For data going back to 2000-10-01, use either the Custom Award Download feature on the website or one of our download or bulk_download API endpoints as listed on https://api.usaspending.gov/docs/endpoints. "]}%
# (whatsapp_rag) ➜  fed_freeze_hack git:(main) ✗ curl -X GET "https://api.usaspending.gov/api/v2/recipient/34228757-4b3c-8dac-90bb-a06834ec884a-C/" \
#   -H "Accept: application/json"
# {"name":"CORICHIA BRISCO ENTERPRISES LLC","alternate_names":[],"duns":"118140624","uei":"KMLTRR8Y96L9","recipient_id":"34228757-4b3c-8dac-90bb-a06834ec884a-C","recipient_level":"C","parent_id":"34228757-4b3c-8dac-90bb-a06834ec884a-P","parent_name":"CORICHIA BRISCO ENTERPRISES LLC","parent_duns":"118140624","parent_uei":"KMLTRR8Y96L9","parents":[{"parent_duns":"118140624","parent_name":"CORICHIA BRISCO ENTERPRISES LLC","parent_id":"34228757-4b3c-8dac-90bb-a06834ec884a-P","parent_uei":"KMLTRR8Y96L9"}],"business_types":["black_american_owned_business","category_business","corporate_entity_not_tax_exempt","economically_disadvantaged_women_owned_small_business","limited_liability_corporation","minority_owned_business","other_than_small_business","self_certified_small_disadvanted_business","service_disabled_veteran_owned_business","small_business","special_designations","us_owned_business","veteran_owned_business","woman_owned_business","women_owned_small_business"],"location":{"address_line1":"9 APPLE BERRY CV","address_line2":null,"address_line3":null,"foreign_province":null,"city_name":"LITTLE ROCK","county_name":null,"state_code":"AR","zip":"72206","zip4":"6999","foreign_postal_code":null,"country_name":"UNITED STATES","country_code":"USA","congressional_code":"02"},"total_transaction_amount":17518.75,"total_transactions":3,"total_face_value_loan_amount":0.0,"total_face_value_loan_transactions":0}%
