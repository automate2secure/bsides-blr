import json
import csv
import os
import sys

def parse_json_to_csv(json_file, csv_file):
    try:
        # Check if the JSON file exists
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"Error: The file {json_file} does not exist.")
        
        # Open the large JSON file and load its content
        with open(json_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                raise ValueError(f"Error: The file {json_file} is not a valid JSON file.")

        # Check if the JSON data is a list of records
        if not isinstance(data, list):
            raise ValueError("Error: The JSON data is not in the expected list format.")

        # Open the CSV file for writing
        with open(csv_file, 'w', newline='', encoding='utf-8') as csv_f:
            # Create a CSV DictWriter instance
            writer = csv.DictWriter(csv_f, fieldnames=data[0].keys())
            writer.writeheader()

            # Write all rows to the CSV
            writer.writerows(data)
        
        print(f"Data successfully written to {csv_file}")
    
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except ValueError as ve_error:
        print(ve_error)
    except PermissionError:
        print(f"Error: Permission denied when accessing {csv_file}. Check your file permissions.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    # Check if enough arguments are passed
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_json_file> <output_csv_file>")
        sys.exit(1)
    
    # Retrieve command-line arguments
    json_file = sys.argv[1]
    csv_file = sys.argv[2]

    # Call the function to parse and write the data
    parse_json_to_csv(json_file, csv_file)

if __name__ == "__main__":
    main()
