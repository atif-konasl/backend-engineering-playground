#!/usr/bin/env bash
set -euo pipefail

HOST=${1:-127.0.0.1}
PORT=${2:-9002}
MESSAGE=${3:-"Hello from UDP client at $(date +%T)"}

echo "=========================================================="
echo " Sending UDP Datagram to ${HOST}:${PORT}"
echo " Message: '${MESSAGE}'"
echo "=========================================================="
echo "Notice: We do NOT need to wait for a server handshake."
echo "Even if the server is offline, this command succeeds immediately"
echo "without waiting for an ACK (Fire-and-Forget)."
echo "----------------------------------------------------------"

echo "${MESSAGE}" | nc -u -w 1 "${HOST}" "${PORT}"
echo "Datagram dispatched."
