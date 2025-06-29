#!/usr/bin/env python3
"""
Simple launch script for blockchain with enhanced dashboard
One-click solution to start blockchain and open dashboard
"""

import subprocess
import sys
import time
import webbrowser
import os

def print_banner():
    """Print startup banner"""
    print("=" * 70)
    print("🚀 BLOCKCHAIN DASHBOARD LAUNCHER")
    print("=" * 70)
    print("🔗 Starting Production Blockchain with Enhanced Dashboard...")
    print()

def check_files():
    """Check if required files exist"""
    required_files = [
        'blockchain.py',
        'enhanced_blockchain_dashboard.html'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING!")
            missing.append(file)
    
    return len(missing) == 0

def start_blockchain():
    """Start the blockchain server"""
    print("\n🔧 Starting blockchain server...")
    try:
        # Start blockchain in background
        process = subprocess.Popen(
            [sys.executable, 'blockchain.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Give it time to start
        time.sleep(3)
        
        # Check if it's still running
        if process.poll() is None:
            print("✅ Blockchain server started successfully!")
            return process
        else:
            print("❌ Failed to start blockchain server")
            return None
            
    except Exception as e:
        print(f"❌ Error starting blockchain: {e}")
        return None

def open_dashboard():
    """Open the dashboard in browser"""
    print("\n🌐 Opening blockchain dashboard...")
    try:
        webbrowser.open('http://localhost:5000')
        print("✅ Dashboard opened in browser")
        print("📍 URL: http://localhost:5000")
    except Exception as e:
        print(f"⚠️  Could not open browser: {e}")
        print("📍 Please open http://localhost:5000 manually")

def print_instructions():
    """Print usage instructions"""
    print("\n" + "=" * 70)
    print("🎯 QUICK START INSTRUCTIONS")
    print("=" * 70)
    print("1. 🖥️  Click 'Start Node' in the Node Management section")
    print("2. 💸 Create a test transaction (genesis → alice)")
    print("3. ⛏️  Mine a block to process transactions")
    print("4. 💰 View wallet balances")
    print("5. 🔗 Explore the blockchain")
    print()
    print("🎮 QUICK ACTIONS:")
    print("   • Use the 'Quick Actions' buttons for one-click operations")
    print("   • Try 'Send Test Transaction' → 'Mine Block'")
    print("   • View real-time status in the status bar")
    print()
    print("📚 FEATURES:")
    print("   ✨ User-friendly interface with visual feedback")
    print("   ✨ Real-time blockchain status monitoring")
    print("   ✨ Complete transaction and mining workflow")
    print("   ✨ Blockchain explorer with detailed transaction view")
    print("   ✨ Multi-wallet management")
    print("   ✨ Network node management")
    print()
    print("⚠️  Press Ctrl+C to stop the blockchain server")
    print("=" * 70)

def main():
    """Main launcher function"""
    print_banner()
    
    # Check files
    print("📋 Checking required files...")
    if not check_files():
        print("\n❌ Missing required files. Please ensure all files are present.")
        input("Press Enter to exit...")
        return
    
    print("\n✅ All required files found!")
    
    # Start blockchain
    process = start_blockchain()
    if not process:
        print("\n❌ Failed to start blockchain. Check for errors above.")
        input("Press Enter to exit...")
        return
    
    # Open dashboard
    time.sleep(1)
    open_dashboard()
    
    # Show instructions
    print_instructions()
    
    # Keep running
    try:
        print("\n⏳ Blockchain is running... Dashboard is ready!")
        print("   Monitor the dashboard for live updates")
        print("   Check connection status in top-right corner")
        print()
        
        # Wait for user interrupt
        while True:
            time.sleep(1)
            # Check if process died
            if process.poll() is not None:
                print("\n⚠️  Blockchain process has stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down blockchain...")
        
    finally:
        # Clean shutdown
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
                print("✅ Blockchain stopped successfully")
            except subprocess.TimeoutExpired:
                process.kill()
                print("⚠️  Blockchain force-stopped")
        
        print("\n👋 Thank you for using the Blockchain Dashboard!")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
