#!/usr/bin/env bash
set -euo pipefail

HOST=${1:-127.0.0.1}
PORT=${2:-8080}

echo "=========================================================="
echo " Demonstrating HTTP Keep-Alive (Persistent TCP Connection)"
echo " Sending 2 HTTP Requests over ONE single TCP Socket"
echo "=========================================================="
echo "Notice in server output:"
echo " - Only ONE '[TCP Connection ESTABLISHED]' message appears."
echo " - Request #1 and Request #2 share the exact same connection_id!"
echo "----------------------------------------------------------"

(
  # Request 1: keep connection alive
  printf "GET /first HTTP/1.1\r\nHost: ${HOST}:${PORT}\r\nConnection: keep-alive\r\n\r\n"
  sleep 1
  # Request 2: close connection after response
  printf "GET /second HTTP/1.1\r\nHost: ${HOST}:${PORT}\r\nConnection: close\r\n\r\n"
) | nc "${HOST}" "${PORT}"
