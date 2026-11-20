#!/usr/bin/env python3
"""
Interactive All-in-One Runner for Load Balancing Labs.
Starts background worker fleet, executes simulations, and cleans up automatically.
"""

import subprocess
import time
import sys
import os

DIR = os.path.dirname(os.path.abspath(__file__))

def start_fleet():
    print("[*] Launching 3 background worker nodes (ports 8001, 8002, 8003)...")
    proc = subprocess.Popen([sys.executable, os.path.join(DIR, "backend_fleet.py")])
    time.sleep(1.2) # Allow servers to bind ports
    return proc

def main():
    fleet_proc = None
    try:
        fleet_proc = start_fleet()
        print("\n" + "="*60)
        print(" Choose which load balancing simulation to run:")
        print(" 1) Smart Client-Side Load Balancing (Zero-Hop Round Robin)")
        print(" 2) Smart Client-Side Load Balancing (Pick of 2 Choices / P2C)")
        print(" 3) DNS Round-Robin & TTL Caching Simulation")
        print(" 4) Run All Simulations Sequentially")
        print("="*60)
        
        choice = sys.argv[1] if len(sys.argv) > 1 else input("Enter choice [1-4] (default: 4): ").strip()
        if not choice:
            choice = "4"

        if choice in ["1", "4"]:
            print("\n>>> RUNNING TEST 1: Smart Client Round-Robin")
            subprocess.run([sys.executable, os.path.join(DIR, "smart_client_balancer.py"), "round_robin"])
            time.sleep(1)

        if choice in ["2", "4"]:
            print("\n>>> RUNNING TEST 2: Smart Client Pick-of-2-Choices (P2C)")
            subprocess.run([sys.executable, os.path.join(DIR, "smart_client_balancer.py"), "p2c"])
            time.sleep(1)

        if choice in ["3", "4"]:
            print("\n>>> RUNNING TEST 3: DNS Round-Robin & Stale Cache")
            subprocess.run([sys.executable, os.path.join(DIR, "simulate_dns_round_robin.py")])

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        if fleet_proc:
            print("\n[*] Cleaning up backend fleet...")
            fleet_proc.terminate()
            fleet_proc.wait()
            print("[*] Done.")

if __name__ == "__main__":
    main()
