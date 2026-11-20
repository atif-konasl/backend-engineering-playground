#!/usr/bin/env bash
set -euo pipefail

PORT=${1:-9001}

echo "=========================================================="
echo " Starting TCP Server with Netcat (nc)"
echo " Listening on: 127.0.0.1:${PORT}"
echo "=========================================================="
echo "Note: TCP is a STATEFUL connection."
echo "1. Run './connect_tcp_client.sh' in a separate terminal window."
echo "2. Run './inspect_sockets.sh' in a third terminal to see ESTABLISHED state."
echo "3. Type any message and press Enter to chat bidirectionally."
echo "4. Press Ctrl+C to terminate the server."
echo "----------------------------------------------------------"

# -l: Listen mode
# -k: Keep listening for multiple connections (macOS BSD nc)
# -v: Verbose output
nc -v -l -k 127.0.0.1 "${PORT}"
