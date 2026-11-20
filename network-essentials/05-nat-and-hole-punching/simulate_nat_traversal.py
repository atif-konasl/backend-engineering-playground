#!/usr/bin/env python3
"""
Interactive WebRTC & NAT Traversal Simulation.
Simulates:
1. Alice and Bob in separate private home networks behind NAT Routers.
2. The Failure Mode: Why direct P2P fails due to unsolicited inbound firewall drops.
3. The Solution: STUN + UDP Hole Punching opening bidirectional NAT states.
"""

import socket
import time
import threading
import sys
from simulated_nat_router import SimulatedNATRouter

# Network Layout Ports:
# Alice (LAN: 6001) -> Router A (LAN: 7001, WAN: 8001)
# Bob   (LAN: 6002) -> Router B (LAN: 7002, WAN: 8002)

def run_simulation():
    print("======================================================================")
    print(" 🌐 WebRTC & NAT Traversal Interactive Simulation")
    print("======================================================================")
    print("Topology:")
    print(" [Alice: 192.168.1.15:6001] -> [Router A (Public WAN: 8001)]")
    print("                                      │ (The Internet)")
    print(" [Bob:   192.168.1.20:6002] -> [Router B (Public WAN: 8002)]")
    print("======================================================================\n")

    # 1. Start Simulated Routers
    router_a = SimulatedNATRouter("Router-A (Alice's Home)", lan_port=7001, wan_port=8001)
    router_b = SimulatedNATRouter("Router-B (Bob's Home)",   lan_port=7002, wan_port=8002)
    router_a.start()
    router_b.start()
    time.sleep(0.5)

    # 2. Setup Alice and Bob client sockets
    alice_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    alice_sock.bind(("127.0.0.1", 6001))

    bob_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bob_sock.bind(("127.0.0.1", 6002))

    bob_received_messages = []
    def bob_listener():
        while True:
            try:
                data, _ = bob_sock.recvfrom(2048)
                msg = data.decode('utf-8', errors='replace')
                bob_received_messages.append(msg)
                print(f"\n\033[92m[BOB RECEIVED P2P MESSAGE!]\033[0m: '{msg}'\n")
            except Exception:
                break

    threading.Thread(target=bob_listener, daemon=True).start()

    # ------------------------------------------------------------------
    # EXPERIMENT 1: The Failure Mode (Why Peers Cannot Speak Directly)
    # ------------------------------------------------------------------
    print("\n" + "="*70)
    print(" 🔴 EXPERIMENT 1: Alice tries to connect directly to Bob")
    print("======================================================================")
    print("Scenario: Alice knows Bob's home router is at WAN port 8002.")
    print("Alice sends a packet through her router destined for Bob's router...")
    time.sleep(1.5)

    # Alice sends through Router A LAN (7001), targeting Bob's WAN (8002)
    # Format: "DEST_PORT:PAYLOAD"
    alice_sock.sendto(b"8002:Hey Bob, can you hear me?", ("127.0.0.1", 7001))
    time.sleep(1.5)

    print("\n--- EXPERIMENT 1 RESULT ---")
    if not bob_received_messages:
        print("❌ BOB RECEIVED NOTHING!")
        print("EXPLANATION:")
        print("1. Alice's packet reached Router B (Bob's home router).")
        print("2. But Router B looked up its NAT table and found NO entry for Alice.")
        print("3. Because routers reject unsolicited inbound connections for security,")
        print("   Router B dropped Alice's packet into the void.")
        print("4. This is why standard P2P fails over the internet without WebRTC!")
    print("="*70)

    time.sleep(2)

    # ------------------------------------------------------------------
    # EXPERIMENT 2: The WebRTC Solution (UDP Hole Punching)
    # ------------------------------------------------------------------
    print("\n" + "="*70)
    print(" 🟢 EXPERIMENT 2: WebRTC UDP Hole Punching (ICE / STUN in Action)")
    print("======================================================================")
    print("Step 1: Alice and Bob both contact a STUN server to learn their public WAN endpoints.")
    print("Step 2: A signaling server (over WebSocket) tells Bob: 'Alice is at WAN 8001'.")
    print("Step 3: Bob sends an outbound packet to Alice's WAN port (8001).")
    print("        --> This forces Router B to create a NAT entry: 'Allow traffic from 8001'!")
    print("        (A hole is punched in Bob's firewall!)")
    time.sleep(2)

    # Bob sends an outbound packet through Router B towards Router A's WAN (8001)
    print("\n[*] Bob punches a hole by sending outbound packet to Router A (8001)...")
    bob_sock.sendto(b"8001:PUNCH_HOLE", ("127.0.0.1", 7002))
    time.sleep(1.5)

    print("\n[*] Now Alice sends her real WebRTC audio/video packet to Bob's WAN (8002)...")
    alice_sock.sendto(b"8002:Hello Bob! WebRTC Direct P2P Audio Stream Connected!", ("127.0.0.1", 7001))
    time.sleep(1.5)

    print("\n--- EXPERIMENT 2 RESULT ---")
    if bob_received_messages:
        print("✅ SUCCESS! Bob received Alice's packet directly!")
        print("EXPLANATION:")
        print("1. Because Bob previously sent an outbound packet towards Alice's router,")
        print("   Router B's NAT table considered Alice's return packet part of an existing session.")
        print("2. Router B performed DNAT (Destination NAT) and delivered the packet to Bob's laptop.")
        print("3. Direct peer-to-peer communication is now established without any relay server!")
    print("="*70)

    # Teardown
    router_a.stop()
    router_b.stop()
    alice_sock.close()
    bob_sock.close()
    print("\nSimulation completed successfully.\n")

if __name__ == "__main__":
    run_simulation()
