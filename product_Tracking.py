import requests
import json


def add_tracking(api_key, tracking_data):
    url = f"https://api.keepa.com/tracking?key={api_key}&type=add"
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps(tracking_data)

    response = requests.post(url, headers=headers, data=payload)
    return response.json()


def get_tracking(api_key, asin):
    url = f"https://api.keepa.com/tracking?key={api_key}&type=get&asin={asin}"

    response = requests.get(url)
    return response.json()


api_key = 'API_KEY'

tracking_data = {
    "asin": "B09NW8WH68",
    "ttl": 0,
    "expireNotify": True,
    "desiredPricesInMainCurrency": True,
    "mainDomainId": 1,
    "updateInterval": 1,
    "thresholdValues": [
        {
            "thresholdValue": 75,  # 25% decrease (75% of original price)
            "domain": 1,
            "csvType": 2,
            "isDrop": True
        },
        {
            "thresholdValue": 70,  # 30% decrease (70% of original price)
            "domain": 1,
            "csvType": 2,
            "isDrop": True  # Tracking value drops
        }
    ],
    "notifyIf": [],
    "notificationType": [False, False, False, False, False, True, False],
    "individualNotificationInterval": -1
}

asin = 'B09NW8WH68'

# Add tracking
add_response = add_tracking(api_key, tracking_data)
print("Add Tracking Response:")
print(add_response)

# Get tracking information
get_response = get_tracking(api_key, asin)
print("\nGet Tracking Response:")
print(get_response)

# ********************************** For CVS ***********************************************

# import csv
# import requests
# import json
#
#
# def add_tracking(api_key, tracking_data):
#     url = f"https://api.keepa.com/tracking?key={api_key}&type=add"
#     headers = {'Content-Type': 'application/json'}
#     payload = json.dumps(tracking_data)
#
#     response = requests.post(url, headers=headers, data=payload)
#     return response.json()
#
#
# def get_tracking(api_key, asin):
#     url = f"https://api.keepa.com/tracking?key={api_key}&type=get&asin={asin}"
#     response = requests.get(url)
#     return response.json()
#
#
# api_key = 'API_KEY'
#
# csv_filename = 'ASIN.csv'
#
# with open(csv_filename, 'r') as csv_file:
#     csv_reader = csv.reader(csv_file)
#     next(csv_reader)
#     for row in csv_reader:
#         asin = row[0]
#         tracking_data = {
#             "asin": asin,
#             "ttl": 0,
#             "expireNotify": True,
#             "desiredPricesInMainCurrency": True,
#             "mainDomainId": 1,
#             "updateInterval": 1,
#             "thresholdValues": [
#                 {
#                     "thresholdValue": 75,  # 25% decrease (75% of original price)
#                     "domain": 1,
#                     "csvType": 2,
#                     "isDrop": True
#                 },
#                 {
#                     "thresholdValue": 70,  # 30% decrease (70% of original price)
#                     "domain": 1,
#                     "csvType": 2,
#                     "isDrop": True  # Tracking value drops
#                 }
#             ],
#             "notifyIf": [],
#             "notificationType": [False, False, False, False, False, True, False],
#             "individualNotificationInterval": -1
#         }
#
#         add_response = add_tracking(api_key, tracking_data)
#         print(f"Add Tracking Response for ASIN {asin}:")
#         print(add_response)
#
#         get_response = get_tracking(api_key, asin)
#         print(f"\nGet Tracking Response for ASIN {asin}:")
#         print(get_response)
#         print("--------------------------")
