# Lab 02: Crafting Raw HTTP Requests with Netcat (nc)

> **Goal:** Understand that **HTTP is simply plain text sent over a stateful TCP connection**. Demystify what tools like `curl`, Postman, or browsers do under the hood, and observe how `Connection: keep-alive` reuses a single TCP socket across multiple HTTP requests.

---

## 1. Background: The Anatomy of an HTTP/1.1 Request

An HTTP request sent over a TCP socket is strictly formatted text complying with RFC 7230:
1. **Request Line:** `METHOD PATH HTTP_VERSION\r\n` (e.g. `GET /api/v1/ping HTTP/1.1\r\n`)
2. **Headers:** Key-value pairs separated by `\r\n` (e.g. `Host: localhost:8080\r\n`)
3. **Header Terminator:** An empty line (`\r\n\r\n`) signaling that headers are done.
4. **Body (Optional):** Payload bytes (for POST/PUT), length specified by `Content-Length`.

```
GET /api/v1/ping HTTP/1.1\r\n   <── Request Line
Host: localhost:8080\r\n        <── Header 1
Connection: close\r\n           <── Header 2
\r\n                            <── Empty line (Signals end of headers!)
```

---

## 2. Interactive Hands-on

### Step 1: Start the Mock HTTP Server
In **Terminal 1**, run:
```bash
python3 run_mock_server.py
```
*(The server prints raw bytes received, tracks TCP connection IDs, and shows socket open/close events).*

---

### Step 2: Send a Raw GET Request
In **Terminal 2**, run:
```bash
./send_get_request.sh
```

**What you will observe:**
* In Terminal 2, you see the full HTTP response including status code (`HTTP/1.1 200 OK`) and response headers.
* In Terminal 1, you see the exact raw text piped through `nc` into the server's TCP socket.

---

### Step 3: Send a Raw POST Request with JSON Body
In **Terminal 2**, run:
```bash
./send_post_request.sh
```

**Key Takeaway:**
* Notice how `Content-Length: 60` informs the server exactly how many bytes to read after the `\r\n\r\n` boundary. Without this header or chunked encoding, the server wouldn't know when the body ends!

---

### Step 4: Prove HTTP Keep-Alive (Socket Reuse)
In **Terminal 2**, run:
```bash
./test_keep_alive.sh
```

**Key System Design Observation:**
* Look at Terminal 1. Notice that **only one TCP handshake occurred (`TCP Connection #1 ESTABLISHED`)**.
* Both `/first` and `/second` were transmitted over the **same open TCP socket**.
* In HTTP/1.0, every request required a new TCP 3-way handshake (`Connection: close`). HTTP/1.1 introduced `keep-alive` to eliminate this connection overhead!

---

## 3. Manual Practice: Type Raw HTTP Directly via Terminal!

You can connect interactively using `nc` or `telnet` and type the HTTP request by hand:

```bash
nc 127.0.0.1 8080
```
Then paste or type:
```http
GET /hello HTTP/1.1
Host: localhost
Connection: close

```
*(Press Enter **twice** to create the empty line `\r\n\r\n`!)*
