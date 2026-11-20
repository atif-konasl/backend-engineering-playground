#!/usr/bin/env python3
"""
Lightweight Mock HTTP Server for Learning Raw Protocols.
Prints every raw byte, header, and socket connection event.
"""
import socket
import sys

HOST = "127.0.0.1"
PORT = 8080

def run_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(5)

    print(f"==========================================================")
    print(f" Mock HTTP Server listening on http://{HOST}:{PORT}")
    print(f" Ready to inspect raw HTTP requests via nc (netcat)!")
    print(f"==========================================================\n")

    conn_counter = 0

    try:
        while True:
            client_sock, client_addr = server_sock.accept()
            conn_counter += 1
            current_conn_id = conn_counter
            print(f"\n[+] [TCP Connection #{current_conn_id} ESTABLISHED] from {client_addr}")

            # Keep reading while connection is open (handles keep-alive)
            request_num = 0
            while True:
                client_sock.settimeout(5.0) # 5-second idle timeout for keep-alive
                try:
                    data = client_sock.recv(4096)
                except socket.timeout:
                    print(f"[-] [TCP Connection #{current_conn_id}] Keep-alive timeout (5s idle). Closing socket.")
                    break

                if not data:
                    print(f"[-] [TCP Connection #{current_conn_id}] Client closed socket (FIN received).")
                    break

                request_num += 1
                raw_text = data.decode('utf-8', errors='replace')
                print(f"\n--- [Request #{request_num} on TCP Conn #{current_conn_id}] Raw Bytes Received ---")
                for line in raw_text.splitlines():
                    print(f"  > {line}")
                print(f"-------------------------------------------------------------------")

                # Parse simple keep-alive vs close
                is_close = "Connection: close" in raw_text or "HTTP/1.0" in raw_text and "Connection: keep-alive" not in raw_text

                body = (
                    f'{{"status":"ok","message":"Hello from raw Netcat!","connection_id":{current_conn_id},'
                    f'"request_on_this_socket":{request_num}}}\n'
                )
                conn_header = "close" if is_close else "keep-alive"
                response = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: application/json\r\n"
                    f"Content-Length: {len(body.encode('utf-8'))}\r\n"
                    f"Connection: {conn_header}\r\n"
                    f"\r\n"
                    f"{body}"
                )

                client_sock.sendall(response.encode('utf-8'))
                print(f"[<] Sent HTTP 200 OK response (Connection: {conn_header})")

                if is_close:
                    print(f"[-] Closing TCP connection #{current_conn_id} as requested by 'Connection: close'.")
                    break

            client_sock.close()

    except KeyboardInterrupt:
        print("\nServer shutting down gracefully.")
    finally:
        server_sock.close()

if __name__ == "__main__":
    run_server()
