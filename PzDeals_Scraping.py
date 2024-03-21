import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time
from selenium.webdriver.support.wait import WebDriverWait

chromedriver_autoinstaller.install()
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
print('Product URLs stored in "product_urls.csv"')
