# import csv
# import re
#
# pattern = r'(?:dp\/|product\/)([A-Z0-9]{10})'
#
#
# def extract_asin_from_url(url):
#     match = re.search(pattern, url)
#     if match:
#         return match.group(1)
#     else:
#         return None
#
#
# def main():
#     # Open CSV file
#     with open('Pz_LINKS_WITH_ASIN.csv', 'r', newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             url = row['URL']
#             asin = extract_asin_from_url(url)
#             if asin:
#                 print(f"URL: {url} | ASIN: {asin}")
#             else:
#                 print(f"Could not extract ASIN from URL: {url}")
#
#
# if __name__ == '__main__':
#     main()


import csv
import re

pattern = r'(?:dp\/|product\/)([A-Z0-9]{10})'


def extract_asin_from_url(url):
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None


def main():
    with open('Pz_LINKS_WITH_ASIN.csv', 'r', newline='') as infile, open('extracted_asin.csv', 'w',
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


if __name__ == '__main__':
    main()
