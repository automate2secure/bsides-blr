import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def get_website_info(url):
    try:
        print(f"\nFetching URL: {url}")
        response = requests.get(url, timeout=10)

        print("\n--- Basic Stats ---")
        print(f"Status Code     : {response.status_code}")
        print(f"Response Time   : {response.elapsed.total_seconds()} seconds")
        print(f"Final URL       : {response.url}")
        print(f"Content Type    : {response.headers.get('Content-Type', 'Unknown')}")
        print(f"Content Length  : {response.headers.get('Content-Length', 'Unknown')}")

        if "text/html" in response.headers.get("Content-Type", ""):
            soup = BeautifulSoup(response.text, "html.parser")

            # Page Title
            title = (
                soup.title.string.strip()
                if soup.title and soup.title.string
                else "No title found"
            )
            print(f"Page Title      : {title}")

            # Parse Headings
            print("\n--- Headings (First 10) ---")
            for tag in ["h1", "h2"]:
                headings = soup.find_all(tag)
                for i, heading in enumerate(headings[:10], 1):
                    print(f"{tag.upper()} #{i}: {heading.get_text(strip=True)}")

            # Parse Links
            print("\n--- Links (First 10) ---")
            links = soup.find_all("a", href=True)
            for i, link in enumerate(links[:10], 1):
                href = urljoin(url, link["href"])
                text = link.get_text(strip=True) or "[no text]"
                print(f"{i}. {text} -> {href}")
        else:
            print("\nContent is not HTML. Skipping parsing.")

    except requests.exceptions.RequestException as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    url = input("Enter the URL: ").strip()
    if not urlparse(url).scheme:
        url = "http://" + url
    get_website_info(url)
