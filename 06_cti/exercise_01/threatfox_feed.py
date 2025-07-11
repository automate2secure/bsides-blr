import requests
import csv
from io import StringIO

# URL to the CSV feed
url = "https://threatfox.abuse.ch/export/csv/md5/recent/"

try:
    response = requests.get(url)
    response.raise_for_status()

    # Split lines and find the line where the actual CSV header starts
    lines = response.text.splitlines()

    needed_lines = []
    for line in lines:
        if line.startswith('#'):
            if 'first_seen_utc' in line:
                line = line[1:]
            else:
                continue
        needed_lines.append(line)

    csv_data = "\n".join(needed_lines)
    reader = csv.DictReader(StringIO(csv_data))
    
    for row in reader:
        print(f"First Seen UTC   : {row.get('first_seen_utc', 'N/A')}")
        print(f"IOC Value        : {row.get('ioc_value', 'N/A')}")
        print(f"IOC Type         : {row.get('ioc_type', 'N/A')}")
        print(f"Threat Type      : {row.get('threat_type', 'N/A')}")
        print(f"Malware Family   : {row.get('malware_printable', 'N/A')}")
        print(f"Last Seen UTC    : {row.get('last_seen_utc', 'N/A')}")
        print(f"Confidence Level : {row.get('confidence_level', 'N/A')}")
        print(f"Tags             : {row.get('tags', 'N/A')}")
        print("=" * 80)

except Exception as e:
    print(f"Error occurred: {e}")
