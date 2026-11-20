#!/usr/bin/env python3
"""
Smart Client-Side Load Balancer.
Demonstrates:
1. Zero-hop direct connections (no central proxy).
2. Client-side algorithms: Round-Robin and Pick of Two Choices (P2C).
3. Client-side circuit breaking: Auto-detecting failed nodes and updating local pool.
"""

import urllib.request
import urllib.error
import json
import time
import random
import sys

class SmartClient:
    def __init__(self, initial_nodes):
        self.nodes = list(initial_nodes) # Locally cached healthy node pool
        self.dead_nodes = {}            # node -> time_marked_dead
        self.rr_index = 0
        self.node_stats = {n: {"success": 0, "failures": 0} for n in initial_nodes}

    def get_next_node_round_robin(self):
        """Standard Round-Robin over healthy nodes"""
        if not self.nodes:
            raise RuntimeError("All backend nodes are DEAD!")
        node = self.nodes[self.rr_index % len(self.nodes)]
        self.rr_index += 1
        return node

    def get_next_node_p2c(self):
        """Pick of Two Choices (P2C) - Picks two random nodes, chooses the one with fewer failures"""
        if not self.nodes:
            raise RuntimeError("All backend nodes are DEAD!")
        if len(self.nodes) == 1:
            return self.nodes[0]
        n1, n2 = random.sample(self.nodes, 2)
        # Choose the node with lower recorded failures
        return n1 if self.node_stats[n1]["failures"] <= self.node_stats[n2]["failures"] else n2

    def execute_request(self, strategy="round_robin", max_retries=2):
        """Executes a direct HTTP request to the selected node with client-side retry"""
        attempts = 0
        while attempts <= max_retries:
            attempts += 1
            node = self.get_next_node_round_robin() if strategy == "round_robin" else self.get_next_node_p2c()
            url = f"http://{node}/"
            
            start_time = time.time()
            try:
                # Direct connection to the backend node (Zero-Hop!)
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req, timeout=1.0) as resp:
                    latency_ms = (time.time() - start_time) * 1000
                    data = json.loads(resp.read().decode('utf-8'))
                    self.node_stats[node]["success"] += 1
                    return {
                        "status": "SUCCESS",
                        "node": node,
                        "latency_ms": latency_ms,
                        "data": data,
                        "attempts": attempts
                    }
            except Exception as e:
                self.node_stats[node]["failures"] += 1
                print(f"  \033[91m[!] Client detected error connecting directly to {node}: {e}\033[0m")
                print(f"  \033[93m[~] Ejecting {node} from local healthy pool & retrying...\033[0m")
                if node in self.nodes:
                    self.nodes.remove(node)
                    self.dead_nodes[node] = time.time()

        return {"status": "FAILED", "error": "Exceeded max retries across healthy nodes"}

def run_demo(strategy="round_robin", total_requests=10):
    initial_fleet = ["127.0.0.1:8001", "127.0.0.1:8002", "127.0.0.1:8003"]
    client = SmartClient(initial_fleet)

    print("==========================================================")
    print(f" Smart Client-Side Load Balancing ({strategy.upper()})")
    print(f" Initial Locally Cached Nodes: {initial_fleet}")
    print(" Notice: ZERO intermediate proxy hop. Requests go direct!")
    print("==========================================================")

    for i in range(1, total_requests + 1):
        result = client.execute_request(strategy=strategy)
        if result["status"] == "SUCCESS":
            print(f" Req #{i:02d} -> Sent to {result['node']} ({result['latency_ms']:.2f}ms) | Handled by: {result['data']['node']}")
        else:
            print(f" Req #{i:02d} -> FAILED: {result['error']}")
        time.sleep(0.3)

    print("\n--- Final Client-Side Telemetry ---")
    for n, s in client.node_stats.items():
        print(f"  Node {n}: {s['success']} succeeded, {s['failures']} failed")
    print("==========================================================")

if __name__ == "__main__":
    strategy = sys.argv[1] if len(sys.argv) > 1 else "round_robin"
    run_demo(strategy)
