from flask import Flask, render_template, request, jsonify
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from selenium.webdriver.support.wait import WebDriverWait
import json
import requests
chromedriver_autoinstaller.install()


app = Flask(
    __name__,
    static_url_path='/static'
)


@app.route('/')
def home():
    return render_template('/pages/dashboard.html')


@app.route('/add_tracking', methods=['POST'])
def add_tracking_endpoint():
    api_key = 'API_KEY'
    tracking_data = request.json
    add_response = add_tracking(api_key, tracking_data)
    return jsonify(add_response)


def add_tracking(api_key, tracking_data):
    url = f"https://api.keepa.com/tracking?key={api_key}&type=add"
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps(tracking_data)
    response = requests.post(url, headers=headers, data=payload)
    return response.json()


@app.route('/remove_tracking/<asin>', methods=['GET'])
def remove_tracking_endpoint(asin):
    api_key = 'API_KEY'
    remove_response = remove_tracking(api_key, asin)
    return jsonify(remove_response)


def remove_tracking(api_key, asin):
    url = f"https://api.keepa.com/tracking?key={api_key}&type=remove&asin={asin}"
    response = requests.get(url)
    return response.json()


@app.route('/get_named_lists', methods=['GET'])
def get_named_lists_endpoint():
    api_key = 'API_KEY'
    named_lists_response = get_named_lists(api_key)
    return jsonify(named_lists_response)


def get_named_lists(api_key):
    url = f"https://api.keepa.com/tracking?key={api_key}&type=list"
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    return response.json()


@app.route('/get_notifications/<since>', methods=['GET'])
def get_notifications_endpoint(since):
    api_key = 'API_KEY'
    notifications_response = get_notifications(api_key, since)
    return jsonify(notifications_response)


def get_notifications(api_key, since, revise=1):
    url = f"https://api.keepa.com/tracking?key={api_key}&type=notification&since={since}&revise={revise}"
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    return response.json()



if __name__ == '__main__':
    app.run(debug=True)
