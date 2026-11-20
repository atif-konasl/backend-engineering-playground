# Network Essentials & Protocols Playground

A collection of hands-on, runnable simulations designed to give you practical, muscle-memory understanding of networking fundamentals, socket states, raw application protocols, and stateful vs. stateless architectures using `netcat` (`nc`), `lsof`, and Python.

---

## 🛠 Prerequisites

On macOS, `nc` (Netcat), `curl`, `lsof`, and `python3` are already installed.

> **Note on `telnet` vs. `netcat` (`nc`):**  
> Modern macOS does not ship with `telnet` by default. `netcat` (`nc`) is the modern, significantly more powerful tool for socket manipulation, port scanning, and testing raw text protocols.

---

## 🧪 Labs & Simulations Index

| Lab | What You Will Learn & Do | Directory |
| :--- | :--- | :--- |
| **01. Stateful TCP vs. Stateless UDP** | Compare TCP 3-way handshake & `ESTABLISHED` socket states against connectionless UDP datagrams using `nc` and `lsof`. | [`01-stateful-tcp-vs-stateless-udp/`](./01-stateful-tcp-vs-stateless-udp/) |
| **02. Crafting Raw HTTP with Netcat** | Send raw RFC 7230 GET and POST requests by piping plain text into `nc`. Prove TCP socket reuse with `Connection: keep-alive`. | [`02-raw-http-with-netcat/`](./02-raw-http-with-netcat/) |
| **03. Stateful Sockets & Thundering Herd** | Run a multi-client TCP chat room, experience in-memory connection siloing, and simulate a 30-client reconnection storm when a stateful server crashes. | [`03-stateful-chat-and-failover/`](./03-stateful-chat-and-failover/) |
| **04. Port Scanning & Network Diagnostics** | Learn the critical difference between `Connection Refused` (TCP RST) and `Connection Timed Out` (Firewall packet drop). | [`04-port-scanning-and-diagnostics/`](./04-port-scanning-and-diagnostics/) |
| **05. NAT Traversal & UDP Hole Punching** | Demystify why WebRTC P2P fails behind NAT routers, observe unsolicited firewall drops, and see STUN hole punching in action. | [`05-nat-and-hole-punching/`](./05-nat-and-hole-punching/) |

---

## 🚀 Quick Run Order

1. **Test TCP vs UDP Socket States:**
   ```bash
   cd 01-stateful-tcp-vs-stateless-udp
   ./start_tcp_server.sh      # in Terminal 1
   ./connect_tcp_client.sh    # in Terminal 2
   ./inspect_sockets.sh       # in Terminal 3 (observe ESTABLISHED state)
   ```

2. **Send Raw HTTP over Netcat:**
   ```bash
   cd 02-raw-http-with-netcat
   python3 run_mock_server.py # in Terminal 1
   ./send_get_request.sh      # in Terminal 2
   ./test_keep_alive.sh       # in Terminal 2 (observe 2 requests on 1 socket)
   ```

3. **Experience Stateful Sockets & Failover:**
   ```bash
   cd 03-stateful-chat-and-failover
   python3 chat_server.py             # in Terminal 1
   python3 simulate_thundering_herd.py # in Terminal 2 (hold 30 persistent connections)
   # Press Ctrl+C in Terminal 1 to witness the connection stampede
   ```

4. **Run Network Diagnostics:**
   ```bash
   cd 04-port-scanning-and-diagnostics
   ./network_diagnostics.sh
   ```

5. **Simulate NAT Traversal & Hole Punching:**
   ```bash
   cd 05-nat-and-hole-punching
   python3 simulate_nat_traversal.py
   ```
