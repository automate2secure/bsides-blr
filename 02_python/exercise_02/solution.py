# For installing subfinder
# go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

import subprocess
import csv
import os
import time
import argparse


def run_subfinder(domain):
    """
    Run subfinder for a given domain and return the results as a list.
    """
    # Run the subfinder command to get subdomains for the given domain
    command = ["subfinder", "-collect-sources", "-d", f"{domain}", "-silent"]

    try:
        # Run the command and capture the output
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        # Return the list of subdomains (split by newlines)
        return result.stdout.strip().splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error running subfinder for {domain}: {e}")
        return []


def save_to_csv(data, filename="subdomains.csv"):
    """
    Save the results (subdomains) to a CSV file.
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Domain", "Subdomain", "Sources"])
        for domain, subdomains_details in data.items():
            for subdomain in subdomains_details:
                writer.writerow([domain, subdomain[0], subdomain[1]])


def save_to_html(data, filename="subdomains.html"):
    """
    Save the results (subdomains) to an HTML file manually.
    """
    with open(filename, "w", encoding="utf-8") as file:
        # Write the HTML header
        file.write(
            "<html>\n<head>\n<title>Subdomains Results</title>\n</head>\n<body>\n"
        )
        file.write("<h1>Subdomains Discovered</h1>\n")
        file.write("<table border='1' cellpadding='5' cellspacing='0'>\n")
        file.write("<tr><th>Domain</th><th>Subdomain</th><th>Source</th></tr>\n")

        # Write data for each domain and its subdomains
        for domain, subdomains_details in data.items():
            for subdomain in subdomains_details:
                file.write(
                    f"<tr><td>{domain}</td><td>{subdomain[0]}</td><td>{subdomain[1]}</td></tr>\n"
                )

        # Close the table and HTML tags
        file.write("</table>\n</body>\n</html>\n")


def main(domain_list, output_format="csv", output_location="./"):
    """
    Main function to process the list of domains.
    Run subfinder and save the results in the specified format (CSV/HTML).
    """
    subdomains_data = {}

    for domain in domain_list:
        print(f"Running subfinder for {domain}...")
        subdomain_results = run_subfinder(domain)
        if subdomain_results:
            formatted_list = []
            for subdomain_result in subdomain_results:
                print(subdomain_result)
                try:
                    subdomain, sources = subdomain_result.split(",", maxsplit=1)
                except:
                    subdomain = subdomain_result
                    sources = ""
                sources = sources.strip("[]").replace(",", " | ")
                formatted_list.append([subdomain, sources])
            subdomains_data[domain] = formatted_list
        time.sleep(1)  # Sleep to prevent overwhelming Subfinder with too many requests

    # Determine the file name for the output
    output_filename = os.path.join(output_location, f"subdomains.{output_format}")

    # Save results based on user preference
    if output_format == "csv":
        save_to_csv(subdomains_data, output_filename)
    elif output_format == "html":
        save_to_html(subdomains_data, output_filename)
    else:
        print("Unsupported output format. Please choose 'csv' or 'html'.")

    print(f"Results saved to {output_filename}")


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Run Subfinder on a list of domains and save the results."
    )
    parser.add_argument(
        "domains",
        metavar="D",
        type=str,
        nargs="+",
        help="List of domains to run Subfinder on.",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=["csv", "html"],
        default="csv",
        help="Output format (csv or html).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="./",
        help="Directory to save the output file.",
    )

    # Parse arguments
    args = parser.parse_args()

    # Run the main function with the parsed arguments
    main(args.domains, output_format=args.format, output_location=args.output)

    # python3 subdomain_finder.py example.com
    # python3 subdomain_finder.py -f html example.com
