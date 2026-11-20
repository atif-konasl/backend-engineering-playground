#!/usr/bin/env bash
set -euo pipefail

HOST=${1:-127.0.0.1}
PORT=${2:-8080}

echo "=========================================================="
echo " Sending Raw HTTP GET Request via Netcat (nc)"
echo " Target: http://${HOST}:${PORT}/api/v1/ping"
echo "=========================================================="
echo "Raw bytes being piped into nc:"
echo "----------------------------------------------------------"
printf "GET /api/v1/ping HTTP/1.1\r\nHost: ${HOST}:${PORT}\r\nUser-Agent: netcat-raw-client/1.0\r\nAccept: application/json\r\nConnection: close\r\n\r\n"
echo "----------------------------------------------------------"
echo "Server Response:"
echo "----------------------------------------------------------"

printf "GET /api/v1/ping HTTP/1.1\r\nHost: ${HOST}:${PORT}\r\nUser-Agent: netcat-raw-client/1.0\r\nAccept: application/json\r\nConnection: close\r\n\r\n" | nc "${HOST}" "${PORT}"
