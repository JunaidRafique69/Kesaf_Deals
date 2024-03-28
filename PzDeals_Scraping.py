import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

driver = webdriver.Chrome()
product_urls = []

try:
    pages = [x for x in range(0, 1000)]
    for page in pages:
        url = f'https://simplexdeals.com/collections/all-products?page={page}'
        driver.get(url)

        # Wait for products to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='product grid__item medium-up--one-third "
                                                           "col2 small--one-half slide-up-animation animated']"))
        )

        products = driver.find_elements(By.XPATH, "//div[@class='product grid__item medium-up--one-third col2 "
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
                continue  # Continue to the next product
            except StaleElementReferenceException:
                print("Stale element reference encountered, retrying.")
                continue  # Continue to the next product
            except Exception as e:
                print(f"An unexpected error occurred for product: {str(e)}")
                continue  # Continue to the next product
        with open('product_urls_.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Product URL'])
            writer.writerows([[url] for url in product_urls])
        print('Product URLs stored in "product_urls.csv"')

except Exception as ex:
    print(f"An error occurred: {str(ex)}")

finally:
    driver.quit()
