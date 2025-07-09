import re

import requests

CVE_REGEX = re.compile("CVE-[0-9]{4}-[0-9]{4,7}")


def get_valid_cves(filename):
    valid_cves = set()
    with open(filename) as fp:
        for line in fp:
            cve = line.strip().upper()
            if CVE_REGEX.match(cve):
                valid_cves.add(cve)

    return list(valid_cves)


def lookup_cve(cve_id):
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    data = {}
    response = requests.get(url)
    if response.status_code == 200:
        #TODO: Parse the JSON response.
        data = response.json()

    return data


def main(filename):
    valid_cves = get_valid_cves()
    for cve in valid_cves:
        print(f"Looking up: {cve}")
        cve_data = lookup_cve(cve)
        print(f"CVE Data: {cve_data}")


if __name__ == "__main__":
    main("cves.txt")
