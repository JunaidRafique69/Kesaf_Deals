import requests


def remove_tracking(api_key, asin):
    url = f"https://api.keepa.com/tracking?key={api_key}&type=remove&asin={asin}"

    response = requests.get(url)
    return response.json()


api_key = 'API_KEY'
asin_to_remove = 'B075NMXLSS'

remove_response = remove_tracking(api_key, asin_to_remove)
print("Remove Tracking Response:")
print(remove_response)
