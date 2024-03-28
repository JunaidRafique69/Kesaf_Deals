from flask import Flask, render_template
from flask import Flask, jsonify
import csv
import re


app = Flask(
    __name__,
    static_url_path='/static'
)


@app.route('/')
def home():
    return render_template('/pages/dashboard.html')


pattern = r'(?:dp\/|product\/)([A-Z0-9]{10})'


def extract_asin_from_url(url):
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None


@app.route('/extract_asin', methods=['GET'])
def extract_asin_endpoint():
    try:
        with open(r'C:\Users\junai\PycharmProjects\kesafdeals\Pz_LINKS_WITH_ASIN.csv', 'r', newline='') as infile, open(
                'extracted_asin.csv', 'w',
                newline='') as outfile:
            reader = csv.DictReader(infile)
            fieldnames = ['URL', 'ASIN']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                url = row['URL']
                asin = extract_asin_from_url(url)
                if asin:
                    writer.writerow({'URL': url, 'ASIN': asin})

        return jsonify({'message': 'ASIN extracted and stored in "extracted_asin.csv" file.'}), 200

    except Exception as ex:
        return jsonify({'error': str(ex)}), 500


if __name__ == '__main__':
    app.run(debug=True)
