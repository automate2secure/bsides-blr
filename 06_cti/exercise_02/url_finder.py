import argparse
from urllib.parse import urlparse
import requests
import csv
import os


# Function to search for URLs on URLScan.io
def search_urlscan(domain):
    urlscan_url = f"https://urlscan.io/api/v1/search/?q=page.domain.keyword:{domain}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    }

    unique_urls = set()
    try:
        response = requests.get(urlscan_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        if results:
            for result in results:
                try:
                    url = result.get("page", {}).get("url")
                    if not url or url == "original":
                        continue
                    url = url.lower()
                    parsed_url = urlparse(url)
                    unique_urls.add(
                        f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
                    )
                except:
                    continue

        else:
            print(f"No URLs found on URLScan.io for {domain}.")
    except requests.RequestException as e:
        print(f"Error fetching URLScan data: {e}")

    return unique_urls


# Function to get URLs from the Wayback Machine
def search_wayback(domain):
    wayback_url = "http://web.archive.org/cdx/search/cdx"

    params = {
        "url": f"{domain}/*",
        "output": "json",
        "fl": "original",
        "collapse": "urlkey",
        "limit": 1000,
    }

    unique_urls = set()
    try:
        response = requests.get(wayback_url, params=params)
        response.raise_for_status()

        data = response.json()
        for result in data:
            try:
                if not result:
                    continue

                url = result[0].lower()
                parsed_url = urlparse(url)
                unique_urls.add(
                    f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
                )
            except Exception as e:
                print(f"ERRORR: {e}")
                continue
    except requests.RequestException as e:
        print(f"Error fetching Wayback Machine data: {e}")

    return unique_urls


def save_to_csv(domain, urls):
    filename = f"{domain}_urls.csv"

    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="") as csvfile:
        fieldnames = ["url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for url in urls:
            writer.writerow({"url": url})

    print(f"Results saved to {filename}.")


def main():
    parser = argparse.ArgumentParser(
        description="Find URLs for a given domain/subdomain on URLScan.io and Wayback Machine."
    )
    parser.add_argument(
        "domain", type=str, help="The domain or subdomain to search for."
    )
    args = parser.parse_args()

    domain = args.domain

    # Search URLScan.io for the given domain
    urlscan_urls = search_urlscan(domain)
    print(f"Found {len(urlscan_urls)} URL(s) from urlscan.io")

    # Search Wayback Machine for the given domain
    wayback_data = search_wayback(domain)
    print(f"Found {len(wayback_data)} URL(s) from wayback")

    unique_urls = list(urlscan_urls.union(wayback_data))
    print(f"Discovered {len(unique_urls)} unique URL(s)")

    # Save results to CSV file
    save_to_csv(domain, unique_urls)


if __name__ == "__main__":
    main()
