#!/usr/bin/env python3
"""
Backend Server Fleet for Load Balancing Simulation.
Spawns 3 independent HTTP worker nodes on localhost ports 8001, 8002, and 8003.
Each node tracks request counts and can simulate sudden failure.
"""

import sys
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

PORTS = [8001, 8002, 8003]
servers = {}
request_counts = {p: 0 for p in PORTS}

class WorkerHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress noisy default HTTP logging
        return

    def do_GET(self):
        port = self.server.server_port
        request_counts[port] += 1
        
        response_data = {
            "node": f"Worker-Node-{port}",
            "port": port,
            "requests_handled_by_this_node": request_counts[port],
            "status": "HEALTHY",
            "timestamp": time.time()
        }
        
        body = json.dumps(response_data, indent=2).encode('utf-8')
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def start_node(port):
    try:
        httpd = HTTPServer(("127.0.0.1", port), WorkerHandler)
        servers[port] = httpd
        httpd.serve_forever()
    except Exception as e:
        print(f"[!] Error on port {port}: {e}")

def run_fleet():
    print("==========================================================")
    print(" Starting Backend Server Fleet (3 Nodes)")
    print("==========================================================")
    threads = []
    for p in PORTS:
        t = threading.Thread(target=start_node, args=(p,), daemon=True)
        t.start()
        threads.append(t)
        print(f" [+] Worker Node online: http://127.0.0.1:{p}")
    print("----------------------------------------------------------")
    print(" Press Ctrl+C to terminate all worker nodes.")
    print("==========================================================")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping backend fleet...")

if __name__ == "__main__":
    run_fleet()
