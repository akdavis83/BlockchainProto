#!/usr/bin/env python3
"""
Startup script for the blockchain prototype
Provides an easy way to launch the blockchain with different configurations
"""

import subprocess
import sys
import time
import threading
from argparse import ArgumentParser

def start_node(port):
    """Start a blockchain node on the specified port"""
    try:
        cmd = [sys.executable, "blockchain.py", "-p", str(port)]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except Exception as e:
        print(f"Error starting node on port {port}: {e}")
        return None

def print_banner():
    """Print startup banner"""
    print("=" * 60)
    print("🔗 PRODUCTION BLOCKCHAIN PROTOTYPE")
    print("=" * 60)
    print("Starting blockchain nodes...")
    print()

def print_instructions(ports):
    """Print usage instructions"""
    print("\n" + "=" * 60)
    print("✅ BLOCKCHAIN NODES STARTED SUCCESSFULLY")
    print("=" * 60)
    
    for port in ports:
        print(f"🟢 Node running on: http://localhost:{port}")
    
    print("\n📚 Available API Endpoints:")
    print("  GET  /chain                - View the blockchain")
    print("  POST /transactions/new     - Create new transaction") 
    print("  GET  /mine                 - Mine pending transactions")
    print("  GET  /balance/<address>    - Get wallet balance")
    print("  GET  /validate             - Validate blockchain")
    print("  POST /nodes/register       - Register network nodes")
    print("  GET  /nodes/resolve        - Run consensus algorithm")
    print("  GET  /info                 - Blockchain information")
    print("  GET  /wallets              - View all balances")
    
    print("\n🧪 Quick Test Commands:")
    main_port = ports[0]
    print(f"  curl http://localhost:{main_port}/info")
    print(f"  curl http://localhost:{main_port}/chain")
    print(f"  python test_blockchain.py")
    
    print("\n📖 For detailed documentation, see README.md")
    print("\n⚠️  Press Ctrl+C to stop all nodes")

def main():
    parser = ArgumentParser(description="Start blockchain prototype nodes")
    parser.add_argument("-p", "--ports", nargs="+", type=int, default=[5000],
                       help="Ports to run blockchain nodes on (default: 5000)")
    parser.add_argument("--multi", action="store_true",
                       help="Start multiple nodes on ports 5000, 5001, 5002")
    
    args = parser.parse_args()
    
    print_banner()
    
    # Set ports
    if args.multi:
        ports = [5000, 5001, 5002]
    else:
        ports = args.ports
    
    processes = []
    
    try:
        # Start all nodes
        for port in ports:
            print(f"Starting blockchain node on port {port}...")
            process = start_node(port)
            if process:
                processes.append(process)
                time.sleep(1)  # Small delay between starts
            else:
                print(f"Failed to start node on port {port}")
        
        if not processes:
            print("No nodes started successfully. Exiting.")
            return
        
        # Wait a moment for nodes to initialize
        time.sleep(2)
        
        print_instructions(ports)
        
        # Keep running until interrupted
        try:
            while True:
                time.sleep(1)
                # Check if any process has died
                for i, process in enumerate(processes):
                    if process.poll() is not None:
                        print(f"\n⚠️  Node on port {ports[i]} has stopped unexpectedly")
        
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping all blockchain nodes...")
    
    finally:
        # Clean shutdown
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception:
                pass
        
        print("✅ All nodes stopped successfully")

if __name__ == "__main__":
    main()
