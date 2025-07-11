import requests

FEED_URL = "https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt"


def main():
    try:
        response = requests.get(FEED_URL)
        urls = response.text.strip().splitlines()
        for url in urls:
            print(url)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
