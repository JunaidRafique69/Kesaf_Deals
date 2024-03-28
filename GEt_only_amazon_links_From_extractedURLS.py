from flask import Flask, jsonify
import csv

app = Flask(__name__)


def filter_csv(input_file, output_file):
    filtered_rows = []

    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Read the header row
        filtered_rows.append(header)  # Add the header to filtered_rows list

        for row in reader:
            if 'amzn' in row[0].lower() or 'amazon' in row[0].lower():
                filtered_rows.append(row)

    # Write filtered rows to a new CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(filtered_rows)

    return {'message': f'Filtered data saved to "{output_file}"'}, 200


@app.route('/filter_csv', methods=['GET'])
def filter_csv_endpoint():
    input_file = 'merged_output_Pz.csv'  # Replace 'merged_output_Pz.csv' with your actual input CSV file name
    output_file = 'Pz.csv'  # Replace 'Pz.csv' with your desired output CSV file name
    result, status_code = filter_csv(input_file, output_file)
    return jsonify(result), status_code


if __name__ == '__main__':
    app.run(debug=True)
