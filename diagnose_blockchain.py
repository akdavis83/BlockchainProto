#!/usr/bin/env python3
"""
Diagnostic script to troubleshoot blockchain startup issues
Checks dependencies, ports, and runs basic tests
"""

import subprocess
import sys
import socket
import time
import os
import importlib

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"🔍 {title}")
    print("=" * 60)

def check_python_version():
    """Check Python version"""
    print_header("PYTHON VERSION CHECK")
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ required")
        return False
    else:
        print("✅ Python version is compatible")
        return True

def check_dependencies():
    """Check if required Python packages are installed"""
    print_header("DEPENDENCY CHECK")
    
    required_packages = {
        'flask': 'Flask',
        'requests': 'requests'
    }
    
    missing = []
    
    for package, import_name in required_packages.items():
        try:
            importlib.import_module(import_name.lower())
            print(f"✅ {package} - installed")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("To install: pip install " + " ".join(missing))
        return False
    else:
        print("\n✅ All required packages are installed")
        return True

def check_files():
    """Check if blockchain files exist"""
    print_header("FILE CHECK")
    
    required_files = [
        'blockchain.py',
        'enhanced_blockchain_dashboard.html'
    ]
    
    optional_files = [
        'blockchain_dashboard.html',
        'test_blockchain.py',
        'requirements.txt'
    ]
    
    missing_required = []
    
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size} bytes)")
        else:
            print(f"❌ {file} - MISSING")
            missing_required.append(file)
    
    print("\nOptional files:")
    for file in optional_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size} bytes)")
        else:
            print(f"⚠️  {file} - not found")
    
    return len(missing_required) == 0

def check_port_availability(port):
    """Check if a port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except socket.error:
        return False

def check_ports():
    """Check port availability"""
    print_header("PORT AVAILABILITY CHECK")
    
    ports_to_check = [5000, 5001, 5002]
    
    for port in ports_to_check:
        if check_port_availability(port):
            print(f"✅ Port {port} - available")
        else:
            print(f"❌ Port {port} - in use")
            
            # Try to find what's using the port
            try:
                result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
                lines = result.stdout.split('\n')
                for line in lines:
                    if f':{port}' in line and 'LISTENING' in line:
                        print(f"   🔍 Process using port {port}: {line.strip()}")
                        break
            except:
                pass

def test_blockchain_syntax():
    """Test if blockchain.py has syntax errors"""
    print_header("SYNTAX CHECK")
    
    try:
        result = subprocess.run([sys.executable, '-m', 'py_compile', 'blockchain.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ blockchain.py - no syntax errors")
            return True
        else:
            print("❌ blockchain.py - syntax errors found:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error checking syntax: {e}")
        return False

def test_blockchain_import():
    """Test if blockchain.py can be imported"""
    print_header("IMPORT TEST")
    
    try:
        # Try to import the blockchain module
        sys.path.insert(0, os.getcwd())
        
        # First, try a basic import test
        result = subprocess.run([sys.executable, '-c', 'import blockchain'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ blockchain.py imports successfully")
            return True
        else:
            print("❌ blockchain.py import failed:")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Import test timed out")
        return False
    except Exception as e:
        print(f"❌ Error during import test: {e}")
        return False

def test_blockchain_startup():
    """Test starting blockchain for a short time"""
    print_header("STARTUP TEST")
    
    try:
        print("🔧 Attempting to start blockchain...")
        
        # Start blockchain process
        process = subprocess.Popen([sys.executable, 'blockchain.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a few seconds
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Blockchain started successfully")
            
            # Try to connect
            try:
                import requests
                response = requests.get('http://localhost:5000/info', timeout=5)
                if response.status_code == 200:
                    print("✅ Blockchain responding to requests")
                    print(f"📊 Response: {response.json()}")
                else:
                    print(f"⚠️  Blockchain started but returned status {response.status_code}")
            except Exception as e:
                print(f"⚠️  Blockchain started but connection failed: {e}")
            
            # Stop the process
            process.terminate()
            try:
                process.wait(timeout=5)
                print("✅ Blockchain stopped cleanly")
            except subprocess.TimeoutExpired:
                process.kill()
                print("⚠️  Had to force-stop blockchain")
            
            return True
            
        else:
            print("❌ Blockchain process exited immediately")
            stdout, stderr = process.communicate()
            print("STDOUT:", stdout.decode())
            print("STDERR:", stderr.decode())
            return False
            
    except Exception as e:
        print(f"❌ Error during startup test: {e}")
        return False

def check_firewall():
    """Check Windows Firewall status"""
    print_header("FIREWALL CHECK")
    
    try:
        result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], 
                              capture_output=True, text=True)
        if 'State' in result.stdout:
            print("🔍 Windows Firewall status detected")
            if 'ON' in result.stdout:
                print("⚠️  Windows Firewall is ON - may block connections")
                print("   Consider adding Python.exe to firewall exceptions")
            else:
                print("✅ Windows Firewall appears to be OFF")
        else:
            print("⚠️  Could not determine firewall status")
    except:
        print("⚠️  Could not check firewall status")

def suggest_fixes():
    """Suggest potential fixes"""
    print_header("SUGGESTED FIXES")
    
    print("🔧 Try these solutions in order:")
    print()
    print("1. INSTALL MISSING DEPENDENCIES:")
    print("   pip install flask requests")
    print()
    print("2. KILL PROCESSES USING PORTS:")
    print("   netstat -ano | findstr :5000")
    print("   taskkill /PID <PID_NUMBER> /F")
    print()
    print("3. RUN AS ADMINISTRATOR:")
    print("   Right-click PowerShell → 'Run as Administrator'")
    print("   cd C:\\Users\\akdav")
    print("   python blockchain.py")
    print()
    print("4. TRY DIFFERENT PORT:")
    print("   python blockchain.py -p 8000")
    print()
    print("5. CHECK ANTIVIRUS:")
    print("   Temporarily disable antivirus")
    print("   Add Python folder to antivirus exceptions")
    print()
    print("6. FIREWALL EXCEPTION:")
    print("   Add Python.exe to Windows Firewall exceptions")
    print("   Or temporarily disable Windows Firewall for testing")

def main():
    """Run all diagnostic tests"""
    print("🚀 BLOCKCHAIN DIAGNOSTIC TOOL")
    print("This will help identify why the blockchain won't start")
    
    # Run all checks
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Files", check_files),
        ("Ports", lambda: (check_ports(), True)[1]),  # Always return True
        ("Syntax", test_blockchain_syntax),
        ("Import", test_blockchain_import),
        ("Startup", test_blockchain_startup),
        ("Firewall", lambda: (check_firewall(), True)[1])  # Always return True
    ]
    
    results = {}
    
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"❌ Error in {name} check: {e}")
            results[name] = False
    
    # Summary
    print_header("DIAGNOSTIC SUMMARY")
    
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    failed_checks = [name for name, passed in results.items() if not passed]
    
    if failed_checks:
        print(f"\n⚠️  Failed checks: {', '.join(failed_checks)}")
        suggest_fixes()
    else:
        print("\n🎉 All checks passed! Blockchain should work.")
        print("If you're still having issues, try:")
        print("   python blockchain.py")
        print("   Then open: http://localhost:5000")

if __name__ == "__main__":
    main()
