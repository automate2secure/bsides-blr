import argparse
import os
from time import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import dns.resolver


# Function to resolve a subdomain using dnspython
def resolve_subdomain(domain, subdomain, found_subdomains):
    subdomain_url = f"{subdomain}.{domain}"

    # Try to resolve the subdomain using DNS
    try:
        answers = dns.resolver.resolve(f"{subdomain}.{domain}", "TXT")
        for answer in answers:
            print(f"[+] Found subdomain: {subdomain_url} -> {answer}")
            found_subdomains.append((subdomain_url, str(answer)))
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        pass  # Ignore if no answer or subdomain does not exist


# Function to load a wordlist file
def load_wordlist(wordlist_file):
    if not os.path.isfile(wordlist_file):
        print(f"[ERROR] Wordlist file '{wordlist_file}' not found.")
        exit(1)

    with open(wordlist_file, "r") as file:
        wordlist = [line.strip() for line in file.readlines()]

    return wordlist


# Main function to handle bruteforce with parallelism
def brute_force_dns(domain, wordlist):
    found_subdomains = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for subdomain in wordlist:
            future = executor.submit(
                resolve_subdomain, domain, subdomain, found_subdomains
            )
            futures.append(future)

        # Wait for all futures to complete
        for future in as_completed(futures):
            pass

    return found_subdomains


# Main function to handle arguments and execute the DNS bruteforce process
def main():
    # Set up command-line arguments
    parser = argparse.ArgumentParser(description="DNS Bruteforce Script")
    parser.add_argument(
        "domain", help="The target domain to brute-force subdomains (e.g. example.com)"
    )
    parser.add_argument(
        "-w",
        "--wordlist",
        default="wordlist.txt",
        help="Wordlist file for brute-forcing (default: wordlist.txt)",
    )
    args = parser.parse_args()

    # Load the wordlist
    wordlist = load_wordlist(args.wordlist)

    print(
        f"Starting DNS bruteforce on {args.domain} with wordlist {args.wordlist}...\n"
    )

    # Start measuring time
    start_time = time()

    # Perform DNS bruteforce with parallelism
    found = brute_force_dns(args.domain, wordlist)

    # Output result summary
    print("\nDNS Bruteforce completed in {:.2f} seconds.".format(time() - start_time))

    if found:
        print(f"\n[+] Found subdomains ({len(found)}):")
        for subdomain, answer in found:
            print(f"  - {subdomain} -> {answer}")
    else:
        print("\n[-] No subdomains found.")

    # Final status summary
    print(f"\n[+] Total subdomains tested: {len(wordlist)}")
    print(f"[+] Total subdomains found: {len(found)}")


if __name__ == "__main__":
    main()
