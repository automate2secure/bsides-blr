import requests
import random
import argparse
import os
from urllib.parse import urljoin
from time import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3

urllib3.disable_warnings()

# List of User-Agent strings to randomize between requests
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
]


# Function to perform an HTTP request to test a directory
def test_directory(url, word, found_directories, successful_urls):
    # Ensure the URL ends with a slash
    if not url.endswith("/"):
        url = url + "/"

    target_url = urljoin(url, word)

    headers = {"User-Agent": random.choice(USER_AGENTS)}  # Randomize User-Agent header

    try:
        # Send request while ignoring SSL errors
        response = requests.get(target_url, headers=headers, verify=False)

        # Check for successful responses (status code 200-299 indicates success)
        if 200 <= response.status_code < 300:
            print(
                f"[+] Found directory: {target_url} (Status code: {response.status_code})"
            )
            found_directories.append(target_url)
            if response.status_code == 200:
                successful_urls.append(target_url)  # Collect all 200 status URLs
        else:
            print(f"[-] {target_url} (Status code: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed for {target_url}: {e}")


# Function to load a wordlist file
def load_wordlist(wordlist_file):
    if not os.path.isfile(wordlist_file):
        print(f"[ERROR] Wordlist file '{wordlist_file}' not found.")
        exit(1)

    with open(wordlist_file, "r") as file:
        wordlist = [line.strip() for line in file.readlines()]

    return wordlist


# Main function to handle fuzzing with parallelism
def fuzz_directories(url, wordlist):
    found_directories = []
    successful_urls = []  # To store URLs with status 200

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for word in wordlist:
            future = executor.submit(
                test_directory, url, word, found_directories, successful_urls
            )
            futures.append(future)

        # Wait for all futures to complete
        for future in as_completed(futures):
            pass

    return found_directories, successful_urls


# Main function to handle arguments and execute the fuzzing process
def main():
    # Set up command-line arguments
    parser = argparse.ArgumentParser(
        description="Directory Fuzzing Script"
    )
    parser.add_argument("url", help="The target URL to fuzz (e.g. https://example.com)")
    parser.add_argument(
        "-w",
        "--wordlist",
        default="wordlist.txt",
        help="Wordlist file for fuzzing (default: wordlist.txt)",
    )
    args = parser.parse_args()

    # Load the wordlist
    wordlist = load_wordlist(args.wordlist)

    print(
        f"Starting directory fuzzing on {args.url} with wordlist {args.wordlist}...\n"
    )

    # Start measuring time
    start_time = time()

    # Perform fuzzing with parallelism
    found, successful_urls = fuzz_directories(args.url, wordlist)

    # Output result summary
    print("\nFuzzing completed in {:.2f} seconds.".format(time() - start_time))

    if found:
        print(f"\n[+] Found directories ({len(found)}):")
        for directory in found:
            print(f"  - {directory}")
    else:
        print("\n[-] No directories found.")

    # Print URLs with status 200
    if successful_urls:
        print(f"\n[+] URLs with status 200 ({len(successful_urls)}):")
        for url in successful_urls:
            print(f"  - {url}")
    else:
        print("\n[-] No URLs responded with status 200.")

    # Final status summary
    print(f"\n[+] Total directories tested: {len(wordlist)}")
    print(f"[+] Total URLs found: {len(found)}")
    print(f"[+] Total URLs with status 200: {len(successful_urls)}")


if __name__ == "__main__":
    main()
