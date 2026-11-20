#!/usr/bin/env bash
set -euo pipefail

HOST=${1:-127.0.0.1}
PORT=${2:-8080}

BODY='{"userId": 42, "role": "admin", "event": "user_promoted"}'
BODY_LEN=$(printf "%s" "$BODY" | wc -c | tr -d ' ')

echo "=========================================================="
echo " Sending Raw HTTP POST Request with Body via Netcat (nc)"
echo " Target: http://${HOST}:${PORT}/api/v1/users"
echo " Content-Length: ${BODY_LEN}"
echo "=========================================================="
echo "Raw bytes being piped into nc:"
echo "----------------------------------------------------------"
printf "POST /api/v1/users HTTP/1.1\r\nHost: ${HOST}:${PORT}\r\nContent-Type: application/json\r\nContent-Length: ${BODY_LEN}\r\nConnection: close\r\n\r\n${BODY}"
echo ""
echo "----------------------------------------------------------"
echo "Server Response:"
echo "----------------------------------------------------------"

printf "POST /api/v1/users HTTP/1.1\r\nHost: ${HOST}:${PORT}\r\nContent-Type: application/json\r\nContent-Length: ${BODY_LEN}\r\nConnection: close\r\n\r\n${BODY}" | nc "${HOST}" "${PORT}"
