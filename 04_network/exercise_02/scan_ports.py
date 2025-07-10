import nmap
import csv


nmap_options = "-Pn -n"
ports = "443"


# Function to scan ports
def scan_ports(target_ip):
    nm = nmap.PortScanner()
    scan_result = {}

    result = nm.scan(target_ip, ports=ports, arguments=nmap_options)
    scan_result = []
    for hostname in result["scan"]:
        for port, port_result in (
            result["scan"].get(hostname, {}).get("tcp", {}).items()
        ):
            result = {"port": port, "host": hostname}
            for key, value in port_result.items():
                result[key] = value if isinstance(value, str) else str(value)

            scan_result.append(result)

    return scan_result


# Function to save the scan results to CSV
def save_to_csv(scan_results, filename="port_scan_results.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=scan_results[0].keys())

        # Write header (fieldnames)
        writer.writeheader()

        # Write rows
        writer.writerows(scan_results)


# Main function to control the scanning
def main():
    target_ip = input("Enter the target hostname: ")

    print(f"Scanning ports on {target_ip}")

    # Perform the port scan
    scan_results = scan_ports(target_ip)

    # Save results to CSV
    save_to_csv(scan_results)

    print(f"Scan complete. Results saved to 'port_scan_results.csv'.")


# Run the main function
if __name__ == "__main__":
    main()
