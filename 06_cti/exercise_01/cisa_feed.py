import requests
import json

# URL of the CISA KEV JSON feed
url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad HTTP status codes
    data = response.json()
    
    vulnerabilities = data.get("vulnerabilities", [])
    
    for vuln in vulnerabilities:
        cve_id = vuln.get("cveID", "N/A")
        name = vuln.get("vulnerabilityName", "N/A")
        vendor = vuln.get("vendorProject", "N/A")
        product = vuln.get("product", "N/A")
        description = vuln.get("shortDescription", "N/A")
        date_added = vuln.get("dateAdded", "N/A")

        print(f"\n{'='*60}")
        print(f"CVE ID:           {cve_id}")
        print(f"Vulnerability:    {name}")
        print(f"Product:          {vendor} {product}")
        print(f"Description:      {description}")
        print(f"Date Added:       {date_added}")
        print(f"{'='*60}")

except requests.exceptions.RequestException as e:
    print(f"Failed to fetch data: {e}")
except json.JSONDecodeError:
    print("Failed to parse JSON response.")
