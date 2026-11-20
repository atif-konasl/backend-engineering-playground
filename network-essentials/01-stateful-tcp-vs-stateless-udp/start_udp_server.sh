#!/usr/bin/env bash
set -euo pipefail

PORT=${1:-9002}

echo "=========================================================="
echo " Starting UDP Server with Netcat (nc)"
echo " Listening on: 127.0.0.1:${PORT}"
echo "=========================================================="
echo "Note: UDP is STATELESS."
echo "There is NO handshake, NO connection state, and NO session."
echo "The OS simply receives datagrams and prints them out."
echo "Press Ctrl+C to stop."
echo "----------------------------------------------------------"

# -u: UDP mode
# -l: Listen
nc -u -l 127.0.0.1 "${PORT}"
