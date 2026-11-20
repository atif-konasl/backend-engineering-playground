# Lab 03: Stateful Socket Server & The Thundering Herd Problem

> **Goal:** Experience why **stateful connections** (like WebSockets or persistent TCP sockets) introduce unique architectural challenges in system design: in-memory connection binding, cross-server broadcasting, and the **Thundering Herd** problem during failover.

---

## 1. Background: Why Stateful Servers are Hard to Scale

In a **stateless architecture** (standard REST APIs), any server behind a round-robin load balancer can handle any request. State is stored externally in PostgreSQL or Redis.

In a **stateful architecture** (WebSockets, live chat, real-time gaming):
1. **Connection Memory Footprint:** The server retains a persistent file descriptor and OS socket buffer in RAM for every connected client.
2. **Instance Affinity (Siloing):** If Alice connects to `Server 1` and Bob connects to `Server 2`, `Server 1` cannot directly send a message to Bob because Bob's socket descriptor is in `Server 2`'s memory! (This requires a pub/sub backbone like Redis or Kafka to bridge servers).
3. **The Thundering Herd Problem:** If `Server 1` crashes while holding 50,000 WebSocket connections, all 50,000 clients disconnect at once and hit your load balancer simultaneously with reconnection requests.

---

## 2. Interactive Hands-on

### Part A: Multi-Client Chat via Netcat
1. **Terminal 1: Start the Stateful Chat Server**
   ```bash
   python3 chat_server.py
   ```
2. **Terminal 2: Connect Alice via Netcat**
   ```bash
   nc 127.0.0.1 9003
   ```
   *Type username `Alice` and hit Enter.*
3. **Terminal 3: Connect Bob via Netcat**
   ```bash
   nc 127.0.0.1 9003
   ```
   *Type username `Bob` and hit Enter.*
4. **Chat back and forth:**
   Type messages in Alice's terminal. Notice they appear instantly in Bob's terminal, and vice-versa.

---

### Part B: Simulating the Thundering Herd
1. Keep `chat_server.py` running in **Terminal 1**.
2. In **Terminal 2**, run the connection storm generator:
   ```bash
   python3 simulate_thundering_herd.py
   ```
   *Watch as 30 persistent connections are spawned and held open.*
3. Now go to **Terminal 1** and press `Ctrl+C` to kill the chat server.
4. **Observe the Reconnection Storm:**
   In Terminal 2, all 30 client sockets drop simultaneously and immediately enter an aggressive reconnect loop. In a production cluster with 100,000 clients, this instantaneous spike in CPU and TLS handshakes can take down the new server before it even finishes booting!

---

## 3. How to Solve This in Real System Design

1. **Jitter & Exponential Backoff:** Clients should never reconnect immediately on disconnect. Add a random delay: `Wait = Base * (2 ^ attempt) + random_jitter()`.
2. **Graceful Connection Draining:** Before restarting a server for deployment, stop accepting new connections and disconnect existing clients gradually (e.g., 500 connections per second) rather than dropping them all at once.
3. **Message Broker (Redis Pub/Sub):** Multiple stateful WebSocket servers subscribe to Redis channels to route messages across instances.
