from flask import Flask, render_template, request, jsonify
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from selenium.webdriver.support.wait import WebDriverWait
# chromedriver_autoinstaller.install()


def extract_simplex_data(output_file_path):
    try:
        driver = webdriver.Chrome()
        product_urls = []
        pages = [x for x in range(0, 2)]
        for page in pages:
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
        driver.quit()
        if product_urls:
            with open(output_file_path + ".csv", 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Product URL'])
                writer.writerows([[url] for url in product_urls])
            return {'message': 'Product URLs extracted and stored in "product_urls.csv" file.'}, 200
        else:
            return {'message': 'No product URLs found.'}, 200
    except Exception as ex:
        driver.quit()
        return {'error': str(ex)}, 500


def extract_pzdeals_data(output_file_path):
    try:
        driver = webdriver.Chrome()
        product_urls = []
        page = [x for x in range(0, 2)]
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
        with open(output_file_path + ".csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Product URL'])
            for url in product_urls:
                writer.writerow([url])
        driver.quit()
        return jsonify({'message': 'Product URLs scraped and stored in "product_urls.csv" file.'}), 200
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500