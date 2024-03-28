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


@app.route('/scrape_PzDeals_urls', methods=['GET'])
def scrape_and_store_urls():
    try:
        driver = webdriver.Chrome()
        product_urls = []
        page = [x for x in range(0, 1000)]
        for pn in page:
            url = f'https://www.pzdeals.com/?page={pn}'
            driver.get(url)
            products = driver.find_elements(By.XPATH, "//li[@class=' on-sale text-center']")
            for product in products:
                try:
                    product.click()
                    product_link = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@class='is_desktop']//a"))
                    )
                    url = product_link.get_attribute('href')
                    print(url)
                    product_urls.append(url)
                    driver.back()
                except NoSuchElementException:
                    print("Element not found while processing product, skipping.")
                except StaleElementReferenceException:
                    print("Stale element reference encountered, retrying.")
                except Exception as e:
                    print(f"An unexpected error occurred: {str(e)}")
        with open('product_urls.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Product URL'])
            for url in product_urls:
                writer.writerow([url])
        driver.quit()
        return jsonify({'message': 'Product URLs scraped and stored in "product_urls.csv" file.'}), 200
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


def extract_urls_and_store(csv_file_path, output_file_path):
    try:
        driver = webdriver.Chrome()
        product_urls = []
        page = 0
        while True:
            url = f'https://simplexdeals.com/collections/all-products?page={page}'
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH,
                                                     "//div[@class='product grid__item medium-up--one-third col2 "
                                                     "small--one-half slide-up-animation animated']"))
            )
            products = driver.find_elements(By.XPATH,
                                            "//div[@class='product grid__item medium-up--one-third col2 "
                                            "small--one-half slide-up-animation animated']")

            if len(products) == 0:
                print(f"No more products on page {page}, exiting loop.")
                break
            for product in products:
                try:
                    product.click()
                    product_link = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@class='product-single__cart-submit-wrapper']//a"))
                    )
                    url = product_link.get_attribute('href')
                    print(url)
                    product_urls.append(url)
                    driver.back()

                except NoSuchElementException:
                    print("Element not found while processing product, skipping.")
                    continue
                except StaleElementReferenceException:
                    print("Stale element reference encountered, retrying.")
                    continue
                except Exception as e:
                    print(f"An unexpected error occurred for product: {str(e)}")
                    continue
            page += 1
        driver.quit()
        if product_urls:
            with open(output_file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Product URL'])
                writer.writerows([[url] for url in product_urls])
            return {'message': 'Product URLs extracted and stored in "product_urls.csv" file.'}, 200
        else:
            return {'message': 'No product URLs found.'}, 200
    except Exception as ex:
        driver.quit()
        return {'error': str(ex)}, 500


@app.route('/Simplex_urls_and_store', methods=['GET'])
def extract_urls_endpoint():
    csv_file_path = 'Pz.csv'  # Change to yo`ur CSV file path
    output_file_path = 'product_urls.csv'  # Change to your desired output file path
    result, status_code = extract_urls_and_store(csv_file_path, output_file_path)
    return jsonify(result), status_code


if __name__ == '__main__':
    app.run(debug=True)
