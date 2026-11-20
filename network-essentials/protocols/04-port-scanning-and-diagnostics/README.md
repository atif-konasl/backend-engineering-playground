# Lab 04: Port Scanning & Connection Diagnostics with Netcat

> **Goal:** Master everyday network troubleshooting using `nc` and `lsof`. Learn to distinguish between **"Connection Refused"** (TCP RST) and **"Connection Timed Out"** (Firewall / Security Group packet drop), which is one of the most common debugging skills in distributed systems.

---

## 1. Core Troubleshooting Concepts

| Error Message | What Actually Happened | Root Cause in Production |
| :--- | :--- | :--- |
| **Connection Refused** | The host was reached, but no process was listening on that port. The OS kernel actively replied with a **TCP RST** packet. | Service crashed, wrong port configured, or service bound only to `127.0.0.1` instead of `0.0.0.0`. |
| **Connection Timed Out** | The request was sent, but **zero response packets** came back before the client gave up. | AWS Security Group / Firewall dropping packets silently, wrong subnet route table, or dead IP. |

---

## 2. Interactive Hands-on

Run the automated diagnostics script:
```bash
./network_diagnostics.sh
```

### Key Netcat Flags to Remember:
* `nc -z`: **Zero-I/O mode**. Used for port scanning without sending data.
* `nc -v`: **Verbose output**. Prints whether connection succeeded or failed.
* `nc -w <seconds>`: **Connection timeout**. Prevents hanging forever when packets are silently dropped.

### Everyday Diagnostic Commands:

1. **Test if a database is reachable:**
   ```bash
   nc -z -v -w 3 db.internal.company.com 5432
   ```
2. **Find what process is hogging port 8080:**
   ```bash
   lsof -nP -iTCP:8080 -sTCP:LISTEN
   ```
3. **Scan a port range:**
   ```bash
   nc -z -v 127.0.0.1 8000-8090
   ```
