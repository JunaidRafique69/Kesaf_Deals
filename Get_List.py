import requests
import json


def get_named_lists(api_key):
    url = f"https://api.keepa.com/tracking?key={api_key}&type=listNames"
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers)
    return response.json()


api_key = 'API_Key'

named_lists_response = get_named_lists(api_key)
print("Named Lists Response:")
print(named_lists_response)
