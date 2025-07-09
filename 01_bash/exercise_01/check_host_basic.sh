#!/bin/bash

# Clear output files
> online_hosts.txt

# Get input file from user
read -p "Enter the filename containing hostnames: " filename

# Check if the file exists
if [[ ! -f "$filename" ]]; then
    echo "[!] File not found: $filename"
    exit 1
fi

# Loop through each hostname in the file
# Set the Internal Field Separator to empty to avoid split on space
while IFS= read -r host
do
    echo "Checking $host..."
    # Check if host is online using ping
    if ping -c 1 -W 1 "$host" &> /dev/null; then
        echo "[+] $host is online"
        echo "$host" >> online_hosts.txt
    else
        echo "[-] $host is offline"
    fi
    echo
done < "$filename"

echo "Scan completed. Results saved to online_hosts.txt"
