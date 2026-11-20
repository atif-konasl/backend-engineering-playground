#!/usr/bin/env python3
"""
Stateful Multi-Client Socket Server.
Demonstrates:
1. In-memory connection state (why stateful servers can't easily be scaled horizontally without Redis).
2. Broadcast to all active sockets connected to this server instance.
3. Socket crash/disconnect events.
"""
import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 9003

# IN-MEMORY CONNECTION STATE:
# These live ONLY in the RAM of this specific process.
# Another server instance on port 9004 would NOT have access to these sockets!
clients_lock = threading.Lock()
active_clients = {} # client_socket -> (client_addr, username)

def broadcast(message, sender_sock=None):
    with clients_lock:
        for sock in list(active_clients.keys()):
            if sock != sender_sock:
                try:
                    sock.sendall(message.encode('utf-8'))
                except Exception:
                    # Broken pipe / client abruptly dropped
                    pass

def handle_client(sock, addr):
    sock.sendall(b"==========================================================\n")
    sock.sendall(b" Welcome to the Stateful TCP Chat Room!\n")
    sock.sendall(b" Enter your username: ")
    
    try:
        raw_name = sock.recv(1024).decode('utf-8').strip()
        username = raw_name if raw_name else f"User_{addr[1]}"
        
        with clients_lock:
            active_clients[sock] = (addr, username)
            total = len(active_clients)
            
        print(f"[+] '{username}' connected from {addr}. Active local connections: {total}")
        broadcast(f"\n[SERVER]: *** '{username}' has entered the room. ({total} users online) ***\n", sock)
        sock.sendall(f"Hello {username}! You can start typing messages now. (Ctrl+C to quit)\n".encode('utf-8'))

        while True:
            data = sock.recv(2048)
            if not data:
                break
            msg = data.decode('utf-8').strip()
            if msg:
                print(f"[{username}]: {msg}")
                broadcast(f"[{username}]: {msg}\n", sock)

    except Exception as e:
        pass
    finally:
        with clients_lock:
            info = active_clients.pop(sock, None)
            total = len(active_clients)
        if info:
            u_name = info[1]
            print(f"[-] '{u_name}' disconnected. Remaining local connections: {total}")
            broadcast(f"\n[SERVER]: *** '{u_name}' has left the room. ({total} users online) ***\n")
        sock.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(100)

    print(f"==========================================================")
    print(f" Stateful Socket Server running on {HOST}:{PORT}")
    print(f" Connect via: nc 127.0.0.1 {PORT}")
    print(f" Notice: All client socket descriptors live in this process RAM.")
    print(f"==========================================================")

    try:
        while True:
            sock, addr = server.accept()
            t = threading.Thread(target=handle_client, args=(sock, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\n[!] Server crashing / shutting down!")
        print(f"[!] Closing all {len(active_clients)} active socket connections simultaneously...")
        with clients_lock:
            for s in active_clients:
                try:
                    s.sendall(b"\n[SERVER ERROR]: Server is shutting down. Connection terminated.\n")
                    s.close()
                except Exception:
                    pass
        server.close()
        print("Shutdown complete.")

if __name__ == "__main__":
    main()
