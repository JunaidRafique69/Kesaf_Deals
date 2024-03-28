from flask import Flask, jsonify
import csv
import os
import chromedriver_autoinstaller
from selenium import webdriver

app = Flask(__name__)

chromedriver_autoinstaller.install()


def extract_asin_from_urls(csv_file_path, output_file_path):
    try:
        driver = webdriver.Chrome()
        is_empty = os.stat(csv_file_path).st_size == 0
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            with open(output_file_path, 'a', newline='') as output_file:
                fieldnames = ['URL']
                csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)

                if is_empty:
                    csv_writer.writeheader()

                for row in csv_reader:
                    driver.get(row['URL'])

                    print(f"URL found: {driver.current_url}")

                    csv_writer.writerow({'URL': driver.current_url})

        driver.quit()
        return {'message': 'ASIN extracted and stored in "Pz_ASIN_new.csv" file.'}, 200

    except Exception as ex:
        return {'error': str(ex)}, 500


@app.route('/extract_asin_from_urls', methods=['GET'])
def extract_asin_endpoint():
    csv_file_path = 'Pz_ASIN_new.csv'
    output_file_path = 'Pz_ASIN_new1 .csv'
    result, status_code = extract_asin_from_urls(csv_file_path, output_file_path)
    return jsonify(result), status_code


if __name__ == '__main__':
    app.run(debug=True)
