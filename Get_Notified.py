import requests


def get_notifications(api_key, since, revise=0):
    url = f"https://api.keepa.com/tracking?key={api_key}&type=notification&since={since}&revise={revise}"
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers)
    return response.json()


api_key = 'API_KEY'

since = 1000000  # Example value,

notifications_response = get_notifications(api_key, since)
print("Get Notifications Response:")
print(notifications_response)
