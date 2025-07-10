#!/bin/bash

TARGET="$1"
OUTDIR="${2:-recon_$TARGET}"
REPORT="$OUTDIR/recon_report.md"

# Check dependencies
REQUIRED_TOOLS=(whois dig nmap curl subfinder httpx openssl)
for tool in "${REQUIRED_TOOLS[@]}"; do
    if ! command -v "$tool" &>/dev/null; then
        echo "Missing required tool: $tool"
        exit 1
    fi
done

if [ -z "$TARGET" ]; then
    echo "Usage: $0 <target-domain> [output-dir]"
    exit 1
fi

mkdir -p "$OUTDIR"

echo "# Recon Report for $TARGET" > "$REPORT"
echo "" >> "$REPORT"
echo "Generated: $(date)" >> "$REPORT"
echo "" >> "$REPORT"

### WHOIS
echo "[*] Gathering WHOIS info..."
whois_data=$(whois "$TARGET")
registrar=$(echo "$whois_data" | grep -iE "Registrar:" | head -n1 | cut -d: -f2- | xargs)
created=$(echo "$whois_data" | grep -iE "Creation Date" | head -n1 | cut -d: -f2- | xargs)
expires=$(echo "$whois_data" | grep -iE "Expiry|Expiration Date" | head -n1 | cut -d: -f2- | xargs)

echo "## Domain Info" >> "$REPORT"
echo "- Registrar: ${registrar:-N/A}" >> "$REPORT"
echo "- Created: ${created:-N/A}" >> "$REPORT"
echo "- Expires: ${expires:-N/A}" >> "$REPORT"
echo "" >> "$REPORT"

### DNS Records
echo "[*] Enumerating DNS records..."
echo "## DNS Records" >> "$REPORT"
for record in A MX NS TXT CNAME; do
    echo "- ${record}:" >> "$REPORT"
    dig +short "$TARGET" "$record" | sed 's/^/  - /' >> "$REPORT"
done
echo "" >> "$REPORT"

### Subdomain Enumeration
echo "[*] Discovering subdomains (subfinder)..."
subfinder -d "$TARGET" -silent > "$OUTDIR/subs1.txt"
cat "$OUTDIR/subs1.txt" | sort -u > "$OUTDIR/subdomains.txt"

echo "## Subdomains Found (Total: $(wc -l < "$OUTDIR/subdomains.txt"))" >> "$REPORT"
while read -r sub; do
    ip=$(dig +short "$sub" | head -n1)
    echo "- $sub → ${ip:-Unresolved}" >> "$REPORT"
done < "$OUTDIR/subdomains.txt"
echo "" >> "$REPORT"

### Port Scanning
echo "[*] Running port scan with Nmap..."
nmap -sV -T4 --top-ports 10 -oN  "$OUTDIR/nmap.txt" "$TARGET" > /dev/null

echo "## Open Ports & Services" >> "$REPORT"
echo "| Port | Protocol | Service | Version |" >> "$REPORT"
echo "|------|----------|---------|---------|" >> "$REPORT"
grep "/tcp" "$OUTDIR/nmap.txt" | while read -r line; do
    port=$(echo "$line" | awk '{print $1}')
    proto=$(echo "$line" | awk '{print $2}')
    svc=$(echo "$line" | awk '{print $3}')
    version=$(echo "$line" | cut -d " " -f4-)
    echo "| $port | $proto | $svc | $version |" >> "$REPORT"
done
echo "" >> "$REPORT"

### HTTP Headers and Tech
echo "[*] Getting HTTP headers and technologies..."
curl -s -I "http://$TARGET" > "$OUTDIR/http.txt"
server=$(grep -i "^Server:" "$OUTDIR/http.txt" | cut -d: -f2- | xargs)
powered_by=$(grep -i "^X-Powered-By:" "$OUTDIR/http.txt" | cut -d: -f2- | xargs)

echo "## Web Server Info" >> "$REPORT"
echo "- Server: ${server:-Unknown}" >> "$REPORT"
echo "- X-Powered-By: ${powered_by:-Unknown}" >> "$REPORT"
echo "" >> "$REPORT"

### SSL Certificate Info
echo "[*] Extracting SSL certificate info..."
cert_data=$(echo | openssl s_client -connect "$TARGET:443" -servername "$TARGET" 2>/dev/null | openssl x509 -noout -issuer -dates -subject)
issuer=$(echo "$cert_data" | grep "issuer=" | cut -d= -f2-)
not_before=$(echo "$cert_data" | grep "notBefore=" | cut -d= -f2)
not_after=$(echo "$cert_data" | grep "notAfter=" | cut -d= -f2)
subject=$(echo "$cert_data" | grep "subject=" | cut -d= -f2-)

echo "## SSL Certificate Info" >> "$REPORT"
echo "- Issuer: ${issuer:-N/A}" >> "$REPORT"
echo "- Valid From: ${not_before:-N/A}" >> "$REPORT"
echo "- Valid Until: ${not_after:-N/A}" >> "$REPORT"
echo "- Subject: ${subject:-N/A}" >> "$REPORT"
echo "" >> "$REPORT"

### Done
echo "[*] Recon complete."
echo "Report saved to: $REPORT"
