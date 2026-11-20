#!/usr/bin/env bash
set -euo pipefail

HOST=${1:-127.0.0.1}
PORT=${2:-9001}

echo "=========================================================="
echo " Connecting TCP Client to ${HOST}:${PORT}"
echo "=========================================================="
echo "The 3-way handshake (SYN -> SYN-ACK -> ACK) will execute automatically."
echo "Once connected, type any text and hit Enter to send."
echo "Press Ctrl+C to close the connection (sends FIN)."
echo "----------------------------------------------------------"

nc -v "${HOST}" "${PORT}"
