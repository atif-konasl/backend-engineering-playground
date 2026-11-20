#!/usr/bin/env bash
set -euo pipefail

TCP_PORT=9001
UDP_PORT=9002

echo "=========================================================="
echo " Inspecting Kernel Socket Tables (lsof / netstat)"
echo "=========================================================="
echo ""
echo "=== 1. TCP Sockets on Port ${TCP_PORT} ==="
if lsof -nP -iTCP:${TCP_PORT} 2>/dev/null; then
    echo ""
    echo ">> KEY OBSERVATION FOR TCP:"
    echo "   - (LISTEN) means the server socket is waiting for connections."
    echo "   - (ESTABLISHED) shows BOTH ends: Local IP:Port <-> Remote IP:Port."
    echo "   - This proves TCP is STATEFUL: the OS kernel actively tracks"
    echo "     the pair, buffer memory, and sequence numbers."
else
    echo "No TCP sockets active on port ${TCP_PORT}. (Start ./start_tcp_server.sh first)"
fi

echo ""
echo "----------------------------------------------------------"
echo "=== 2. UDP Sockets on Port ${UDP_PORT} ==="
if lsof -nP -iUDP:${UDP_PORT} 2>/dev/null; then
    echo ""
    echo ">> KEY OBSERVATION FOR UDP:"
    echo "   - Notice there is NO '(ESTABLISHED)' or '(LISTEN)' state!"
    echo "   - The kernel only knows that an application is bound to UDP :${UDP_PORT}."
    echo "   - UDP is STATELESS: It never records who it is talking to."
else
    echo "No UDP sockets active on port ${UDP_PORT}. (Start ./start_udp_server.sh first)"
fi
echo "=========================================================="
