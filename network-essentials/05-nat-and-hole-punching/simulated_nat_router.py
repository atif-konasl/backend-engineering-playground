#!/usr/bin/env python3
"""
Simulated NAT Router & State Table (RFC 4787 / NAT Traversal Lab).
Demonstrates:
1. SNAT (Source NAT): Rewriting internal IP:port to public IP:port.
2. NAT State Table (Mapping outbound connections).
3. The Firewall Drop: Rejecting unsolicited inbound packets that have no NAT table entry.
"""

import socket
import threading
import time
import sys

class SimulatedNATRouter:
    def __init__(self, name, lan_port, wan_port):
        self.name = name
        self.lan_port = lan_port  # Port facing internal home devices
        self.wan_port = wan_port  # Port facing the public internet
        self.public_ip = "198.51.100.1" if "B" in name else "203.0.113.1"
        
        # Sockets
        self.lan_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.lan_sock.bind(("127.0.0.1", self.lan_port))
        
        self.wan_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.wan_sock.bind(("127.0.0.1", self.wan_port))

        # NAT State Table:
        # Key: (remote_host, remote_port) -> Value: (internal_host, internal_port, timestamp)
        self.nat_table = {}
        self.lock = threading.Lock()
        self.running = True

    def print_nat_table(self):
        print(f"\n--- [{self.name} ACTIVE NAT STATE TABLE] ---")
        if not self.nat_table:
            print("  (Empty - No outbound sessions initiated)")
        else:
            print(f"  {'REMOTE PUBLIC ENDPOINT':<30} <---> {'INTERNAL PRIVATE ENDPOINT'}")
            for remote, internal in self.nat_table.items():
                r_str = f"{remote[0]}:{remote[1]}"
                i_str = f"{internal[0]}:{internal[1]}"
                print(f"  {r_str:<30} <---> {i_str}")
        print("--------------------------------------------------\n")

    def handle_outbound_lan_traffic(self):
        """Traffic from internal home devices heading out to the Internet (SNAT)"""
        while self.running:
            try:
                data, internal_addr = self.lan_sock.recvfrom(4096)
                # Payload format expected: "DEST_PORT:actual_message"
                msg_str = data.decode('utf-8', errors='replace')
                if ":" in msg_str:
                    dest_port_str, payload = msg_str.split(":", 1)
                    dest_port = int(dest_port_str)
                    dest_addr = ("127.0.0.1", dest_port)
                else:
                    dest_addr = ("127.0.0.1", 9999)
                    payload = msg_str

                # Record in NAT Table:
                # "We sent a packet to dest_addr, so allow return traffic from dest_addr!"
                with self.lock:
                    self.nat_table[dest_addr] = (internal_addr[0], internal_addr[1], time.time())
                
                print(f"[OUTBOUND] {self.name} received packet from internal {internal_addr}")
                print(f"           --> SNAT Rewrite: Source changed to Public {self.public_ip}:{self.wan_port}")
                print(f"           --> NAT Hole Opened for return traffic from {dest_addr}!")
                self.print_nat_table()

                # Forward out to the public internet
                self.wan_sock.sendto(payload.encode('utf-8'), dest_addr)

            except Exception:
                break

    def handle_inbound_wan_traffic(self):
        """Traffic from the Public Internet attempting to enter the private network (DNAT)"""
        while self.running:
            try:
                data, sender_addr = self.wan_sock.recvfrom(4096)
                payload = data.decode('utf-8', errors='replace')

                # Check NAT Table:
                # Does an entry exist allowing traffic from this sender_addr?
                internal_target = None
                with self.lock:
                    internal_target = self.nat_table.get(sender_addr)

                if internal_target:
                    print(f"\n[INBOUND ALLOWED] {self.name} accepted packet from {sender_addr}!")
                    print(f"                  --> Matching NAT entry found for internal {internal_target[0]}:{internal_target[1]}")
                    print(f"                  --> DNAT Rewrite: Forwarding payload: '{payload}'")
                    # Forward to the internal device
                    self.lan_sock.sendto(payload.encode('utf-8'), (internal_target[0], internal_target[1]))
                else:
                    print(f"\n\033[91m[FIREWALL DROP - SECURITY ALERT!]\033[0m")
                    print(f"  {self.name} received UNSOLICITED inbound packet from {sender_addr}!")
                    print(f"  Payload: '{payload}'")
                    print(f"  REASON: No internal device ever sent outbound traffic to {sender_addr}.")
                    print(f"          The NAT router drops this packet immediately to protect the internal network.")
                    self.print_nat_table()

            except Exception:
                break

    def start(self):
        t1 = threading.Thread(target=self.handle_outbound_lan_traffic, daemon=True)
        t2 = threading.Thread(target=self.handle_inbound_wan_traffic, daemon=True)
        t1.start()
        t2.start()
        print(f"==================================================")
        print(f" {self.name} Running")
        print(f" Internal LAN Interface: 127.0.0.1:{self.lan_port} (Private)")
        print(f" External WAN Interface: {self.public_ip}:{self.wan_port} (Public)")
        print(f"==================================================")

    def stop(self):
        self.running = False
        self.lan_sock.close()
        self.wan_sock.close()

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "Router-A"
    lan = int(sys.argv[2]) if len(sys.argv) > 2 else 7001
    wan = int(sys.argv[3]) if len(sys.argv) > 3 else 8001
    router = SimulatedNATRouter(name, lan, wan)
    router.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{name} shutting down.")
        router.stop()
