#!/usr/bin/env python3
"""
Quick setup script for the blockchain dashboard
Checks dependencies and provides setup instructions
"""

import subprocess
import sys
import os
import webbrowser
import time

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    dependencies = ['flask', 'requests']
    missing = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} is installed")
        except ImportError:
            print(f"❌ {dep} is missing")
            missing.append(dep)
    
    return missing

def install_dependencies(missing):
    """Install missing dependencies"""
    if not missing:
        return True
    
    print(f"\n📦 Installing missing dependencies: {', '.join(missing)}")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def check_files():
    """Check if required files exist"""
    files = [
        'blockchain.py',
        'blockchain_dashboard.html',
        'test_blockchain.py'
    ]
    
    missing = []
    for file in files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} missing")
            missing.append(file)
    
    return len(missing) == 0

def start_blockchain(port=5000):
    """Start the blockchain with dashboard"""
    print(f"\n🚀 Starting blockchain on port {port}...")
    try:
        process = subprocess.Popen([sys.executable, 'blockchain.py', '-p', str(port)])
        time.sleep(3)  # Give it time to start
        
        # Check if process is still running
        if process.poll() is None:
            print(f"✅ Blockchain started successfully!")
            print(f"🌐 Dashboard: http://localhost:{port}")
            print(f"📊 API: http://localhost:{port}/info")
            
            # Try to open browser
            try:
                webbrowser.open(f'http://localhost:{port}')
                print("🔗 Opened dashboard in browser")
            except:
                print("⚠️  Could not open browser automatically")
            
            return process
        else:
            print("❌ Failed to start blockchain")
            return None
    except Exception as e:
        print(f"❌ Error starting blockchain: {e}")
        return None

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🔗 BLOCKCHAIN DASHBOARD SETUP")
    print("=" * 60)
    print("Setting up Production Blockchain Prototype...")
    print()

def print_usage_instructions():
    """Print usage instructions"""
    print("\n" + "=" * 60)
    print("📚 USAGE INSTRUCTIONS")
    print("=" * 60)
    print("1. Dashboard: Browse to http://localhost:5000")
    print("2. Create transactions using the web interface")
    print("3. Mine blocks to process transactions")
    print("4. View blockchain explorer")
    print("5. Check wallet balances")
    print("6. Manage network nodes")
    print()
    print("📝 Quick Test:")
    print("  python test_blockchain.py")
    print()
    print("🔧 Manual API Testing:")
    print("  curl http://localhost:5000/info")
    print("  curl http://localhost:5000/chain")
    print()
    print("⚠️  Press Ctrl+C to stop the blockchain")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return
    
    print()
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        if not install_dependencies(missing):
            return
    
    print()
    
    # Check files
    if not check_files():
        print("\n❌ Missing required files. Please ensure all files are in the same directory.")
        return
    
    print()
    
    # Start blockchain
    process = start_blockchain()
    if not process:
        return
    
    print_usage_instructions()
    
    # Keep running
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping blockchain...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        print("✅ Blockchain stopped successfully")

if __name__ == "__main__":
    main()
