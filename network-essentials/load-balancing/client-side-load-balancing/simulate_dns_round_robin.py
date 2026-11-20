#!/usr/bin/env python3
"""
Simulate DNS Round-Robin & The TTL Caching Dilemma.
Demonstrates:
1. DNS returning rotated IP lists (Round-Robin).
2. The Client connecting to the first IP in the list.
3. The Stale Cache Disaster: What happens when a server crashes during the DNS TTL window!
"""

import urllib.request
import urllib.error
import json
import time

class SimulatedDNSNameserver:
    def __init__(self, records, ttl_seconds=5):
        self.records = list(records)
        self.ttl = ttl_seconds
        self.query_count = 0

    def resolve(self, domain="mycoolapp.com"):
        """Returns the rotated A-records list (Round-Robin)"""
        self.query_count += 1
        # Rotate records
        rotated = self.records[:]
        shift = (self.query_count - 1) % len(self.records)
        rotated = rotated[shift:] + rotated[:shift]
        return {
            "domain": domain,
            "ips": rotated,
            "ttl": self.ttl,
            "resolved_at": time.time()
        }

class StandardBrowserClient:
    def __init__(self, dns_server, name="Browser-1"):
        self.dns = dns_server
        self.name = name
        self.dns_cache = None
        self.cache_expires_at = 0

    def fetch_page(self):
        now = time.time()
        
        # 1. Check local DNS cache
        if not self.dns_cache or now >= self.cache_expires_at:
            print(f"[{self.name}] DNS Cache EXPIRED or empty. Querying DNS Nameserver...")
            res = self.dns.resolve()
            self.dns_cache = res["ips"]
            self.cache_expires_at = now + res["ttl"]
            print(f"[{self.name}] DNS answered: {self.dns_cache} (Cached for {res['ttl']}s TTL)")
        else:
            remaining = int(self.cache_expires_at - now)
            print(f"[{self.name}] Using cached DNS entry ({remaining}s remaining before expiry).")

        # Browser picks the TOP IP from its cached list
        target_ip = self.dns_cache[0]
        url = f"http://{target_ip}/"

        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=0.8) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                print(f"  \033[92m[✓] Success!\033[0m Connected to {target_ip} -> Handled by {data['node']}")
                return True
        except Exception as e:
            print(f"  \033[91m[X] Connection Failed!\033[0m Target {target_ip} unreachable: {e}")
            print(f"      (The browser is trapped hitting the dead IP until its DNS cache expires!)")
            return False

def run_simulation():
    records = ["127.0.0.1:8001", "127.0.0.1:8002", "127.0.0.1:8003"]
    dns = SimulatedDNSNameserver(records, ttl_seconds=4)

    print("==========================================================")
    print(" 🌐 DNS Round-Robin & TTL Caching Simulation")
    print("==========================================================")
    print("Record Pool in DNS Nameserver:", records)
    print("DNS TTL configured to: 4 seconds")
    print("==========================================================\n")

    print("--- PART 1: Demonstrating IP Rotation Across Different Clients ---")
    c1 = StandardBrowserClient(dns, name="Alice (Chrome)")
    c2 = StandardBrowserClient(dns, name="Bob (Safari)")
    c3 = StandardBrowserClient(dns, name="Charlie (Firefox)")

    c1.fetch_page()
    time.sleep(0.5)
    c2.fetch_page()
    time.sleep(0.5)
    c3.fetch_page()
    time.sleep(1.0)

    print("\n" + "="*58)
    print("--- PART 2: The Stale DNS Cache Disaster ---")
    print("Scenario: Alice makes repeated requests.")
    print("Notice what happens while Alice's local DNS cache is still valid.")
    print("==========================================================\n")

    for i in range(1, 6):
        print(f"\n[Alice Request #{i}]")
        c1.fetch_page()
        time.sleep(1.2)

    print("\nSimulation complete.")

if __name__ == "__main__":
    run_simulation()
