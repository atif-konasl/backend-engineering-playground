#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo " Network Diagnostics with Netcat (nc) & lsof"
echo "=========================================================="

echo ""
echo "=== 1. Checking Connection to Common Local Ports ==="
# Test ports 80, 443, 5432 (Postgres), 6379 (Redis), 8080
PORTS=(80 443 5432 6379 8080)
for p in "${PORTS[@]}"; do
    if nc -z -v -w 1 127.0.0.1 "$p" 2>/dev/null; then
        echo "  [OPEN] Port $p on 127.0.0.1 is REACHABLE."
    else
        echo "  [CLOSED/REFUSED] Port $p on 127.0.0.1 is unreachable."
    fi
done

echo ""
echo "----------------------------------------------------------"
echo "=== 2. Connection Refused vs. Timeout Difference ==="
echo "When connecting to a closed port on an active host (127.0.0.1:54321):"
echo "-> The OS kernel immediately replies with a TCP RST (Reset) packet."
time nc -z -v -w 2 127.0.0.1 54321 2>&1 || true

echo ""
echo "When connecting to an unroutable IP (simulating a firewall/Security Group drop):"
echo "-> No response packet ever arrives. nc waits until timeout (-G 1s) expires:"
time nc -z -v -G 1 198.51.100.1 80 2>&1 || true

echo ""
echo "----------------------------------------------------------"
echo "=== 3. Listing All Listening TCP Ports on this Machine ==="
lsof -nP -iTCP -sTCP:LISTEN | head -n 15
echo "=========================================================="
