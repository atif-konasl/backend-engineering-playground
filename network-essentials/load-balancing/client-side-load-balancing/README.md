# Lab 06: Client-Side Load Balancing & DNS Round-Robin

> **Core Insight:** In high-scale distributed systems, not all load balancing happens on a central proxy (like AWS ALB or NGINX).  
> In **Client-Side Load Balancing** (e.g., gRPC, Redis Cluster), the client connects **directly** to backend servers with zero intermediate proxy hops. In **DNS Round-Robin**, the DNS resolver rotates the list of IP addresses returned to client browsers.

---

## 1. Labs Overview

| Script | What It Demonstrates |
| :--- | :--- |
| **`backend_fleet.py`** | Spawns 3 lightweight HTTP worker nodes on `localhost:8001`, `8002`, and `8003`. |
| **`smart_client_balancer.py`** | A "smart client" (like a gRPC client or Redis Cluster driver) that balances requests directly using **Round-Robin** or **Pick-of-2-Choices (P2C)**, and automatically ejects dead nodes. |
| **`simulate_dns_round_robin.py`** | Simulates a DNS nameserver rotating IP lists, and demonstrates the **TTL / Stale Cache failure** when an IP goes down during a cached TTL window. |
| **`run_demo.py`** | Automated all-in-one runner that spins up the fleet, executes the tests, and tears down cleanly. |

---

## 2. Interactive Hands-on

### Option A: The All-in-One Automated Demo (Recommended)
Run the master runner:
```bash
python3 run_demo.py
```
*(Spawns 3 background workers, runs Round-Robin, P2C, and DNS simulations, then shuts down cleanly).*

---

### Option B: Manual Multi-Terminal Experimentation

#### Step 1: Start the Backend Fleet
In **Terminal 1**:
```bash
python3 backend_fleet.py
```
*(Starts 3 nodes listening on ports 8001, 8002, and 8003).*

#### Step 2: Run the Smart Client Balancer
In **Terminal 2**:
```bash
# Test Round-Robin:
python3 smart_client_balancer.py round_robin

# Test Pick-of-2-Choices (P2C):
python3 smart_client_balancer.py p2c
```

**Key System Design Observation:**
* Notice that every request connects **directly** to `127.0.0.1:8001`, `8002`, or `8003`.
* There is **zero intermediate proxy hop**! Latency is sub-millisecond.

#### Step 3: Run the DNS Round-Robin & Stale Cache Simulation
In **Terminal 2**:
```bash
python3 simulate_dns_round_robin.py
```

**Key Observation:**
* Notice how Alice, Bob, and Charlie each receive a different primary IP because the DNS nameserver rotates the list.
* Notice how Alice caches the IP for the duration of the TTL (4 seconds), illustrating why DNS Round-Robin cannot quickly detect a crashed server.
