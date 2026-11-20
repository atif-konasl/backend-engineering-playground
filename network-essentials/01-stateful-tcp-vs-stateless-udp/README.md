# Lab 01: Stateful TCP vs. Stateless UDP

> **Goal:** Experience the difference between a **stateful transport connection (TCP)** and a **stateless transport protocol (UDP)** using `netcat` (`nc`) and kernel socket inspection (`lsof`).

---

## 1. Background

* **TCP is Stateful:**
  Before any data can be exchanged, the client and server must perform a 3-way handshake (`SYN` $\rightarrow$ `SYN-ACK` $\rightarrow$ `ACK`). The operating system kernel creates and manages connection state: sequence numbers, window buffers, and connection lifecycle (`ESTABLISHED`, `FIN_WAIT`, `CLOSE_WAIT`).
* **UDP is Stateless:**
  There is no handshake, no connection establishment, and no tracking. Packets are fired into the network as independent datagrams. The kernel does not maintain an "established" state with any remote peer.

---

## 2. Interactive Hands-on

### Part A: Exploring Stateful TCP

1. **Terminal 1: Start the TCP Server**
   ```bash
   ./start_tcp_server.sh
   ```
   *(Listens on `127.0.0.1:9001` using `nc -l -k`)*

2. **Terminal 2: Inspect Kernel Socket State**
   ```bash
   ./inspect_sockets.sh
   ```
   *Notice the server socket is in `(LISTEN)` mode.*

3. **Terminal 3: Connect a TCP Client**
   ```bash
   ./connect_tcp_client.sh
   ```

4. **Terminal 2: Re-run Socket Inspection**
   ```bash
   ./inspect_sockets.sh
   ```
   *You will now see a second socket in `(ESTABLISHED)` state linking `127.0.0.1:9001` directly to your client's ephemeral port (`127.0.0.1:5xxxx`).*

5. **Chat interactively:**
   Type a message in Terminal 3 and hit Enter. Watch it appear in Terminal 1. Hit `Ctrl+C` in Terminal 3 to tear down the connection.

---

### Part B: Exploring Stateless UDP

1. **Terminal 1: Start the UDP Listener**
   ```bash
   ./start_udp_server.sh
   ```
   *(Listens on `127.0.0.1:9002` using `nc -u -l`)*

2. **Terminal 2: Send a UDP Datagram**
   ```bash
   ./send_udp_datagram.sh 127.0.0.1 9002 "Hello UDP World!"
   ```
   *Notice how the command exits immediately. It did not wait for any connection establishment or ACK.*

3. **Terminal 3: Inspect Sockets**
   ```bash
   ./inspect_sockets.sh
   ```
   *Notice that the UDP entry has **no `(ESTABLISHED)` or `(LISTEN)` state**.*

4. **Test Fire-and-Forget:**
   Stop the UDP server in Terminal 1 (`Ctrl+C`). Now run `./send_udp_datagram.sh`.
   *Notice that sending still succeeds without any error! UDP does not check if the server is alive.*
