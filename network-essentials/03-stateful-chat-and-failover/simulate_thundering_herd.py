#!/usr/bin/env python3
"""
Simulate Thundering Herd / Reconnection Storm
Spawns N concurrent persistent TCP clients.
Observes what happens when a stateful server restarts.
"""
import socket
import time
import threading
import sys

HOST = "127.0.0.1"
PORT = 9003
NUM_CLIENTS = 30

def simulated_client(client_id):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            # Handshake username
            s.recv(1024)
            s.sendall(f"Bot-{client_id}\n".encode('utf-8'))
            
            # Keep reading while connected
            while True:
                data = s.recv(1024)
                if not data:
                    break
        except Exception:
            pass
        finally:
            s.close()

        # Server dropped! Reconnection attempt (Simulated Stampede)
        print(f"[!] Bot-{client_id}: Socket closed! Immediate reconnect attempt...")
        time.sleep(1.0)

def main():
    print(f"==========================================================")
    print(f" Spawning {NUM_CLIENTS} Persistent TCP Client Connections...")
    print(f" Target: {HOST}:{PORT}")
    print(f"==========================================================")

    threads = []
    for i in range(1, NUM_CLIENTS + 1):
        t = threading.Thread(target=simulated_client, args=(i,), daemon=True)
        threads.append(t)
        t.start()
        time.sleep(0.05)

    print(f"\n[+] All {NUM_CLIENTS} clients connected and holding open sockets.")
    print("Now go to the chat_server terminal and press Ctrl+C to kill the server.")
    print("Watch how all clients immediately detect disconnection and stampede back!")
    print("Press Ctrl+C here to terminate simulation.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSimulation ended.")

if __name__ == "__main__":
    main()
