#!/usr/bin/env python3
"""
Improved launch script with better timing and connection handling
"""

import subprocess
import sys
import time
import webbrowser
import requests
import os

def wait_for_blockchain(max_wait=30):
    """Wait for blockchain to be ready with proper timing"""
    print("⏳ Waiting for blockchain to be ready...")
    
    for i in range(max_wait):
        try:
            response = requests.get('http://localhost:5000/info', timeout=2)
            if response.status_code == 200:
                print(f"✅ Blockchain is ready! (took {i+1} seconds)")
                return True
        except:
            pass
        
        print(f"   Checking... ({i+1}/{max_wait})")
        time.sleep(1)
    
    print("❌ Blockchain didn't become ready in time")
    return False

def main():
    """Launch blockchain with improved timing"""
    print("🚀 IMPROVED BLOCKCHAIN LAUNCHER")
    print("=" * 50)
    
    # Start blockchain
    print("🔧 Starting blockchain server...")
    process = subprocess.Popen([sys.executable, 'blockchain.py'])
    
    # Wait for it to be ready
    if wait_for_blockchain():
        print("\n🌐 Opening dashboard...")
        webbrowser.open('http://localhost:5000')
        
        print("\n✅ SUCCESS! Blockchain is running and dashboard is open.")
        print("📍 URL: http://localhost:5000")
        print("\n⚠️  Press Ctrl+C to stop")
        
        try:
            # Keep running
            while True:
                time.sleep(1)
                if process.poll() is not None:
                    print("\n⚠️  Blockchain stopped unexpectedly")
                    break
        except KeyboardInterrupt:
            print("\n🛑 Stopping blockchain...")
            process.terminate()
            print("✅ Stopped successfully")
    else:
        print("❌ Failed to start properly")
        process.terminate()

if __name__ == "__main__":
    main()
