from flask import Flask, jsonify
import csv
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

app = Flask(__name__)

chromedriver_autoinstaller.install()


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
