import csv
import chromedriver_autoinstaller
from selenium import webdriver
import os

chromedriver_autoinstaller.install()
driver = webdriver.Chrome()
csv_file_path = 'Pz.csv'
is_empty = os.stat(csv_file_path).st_size == 0
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    with open('Pz_ASIN_new.csv', 'a', newline='') as output_file:
        fieldnames = ['URL']
        csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        if is_empty:
            csv_writer.writeheader()

        for row in csv_reader:
            driver.get(row['URL'])

            print(f"URL found: {driver.current_url}")

            csv_writer.writerow({'URL': driver.current_url})

driver.quit()
