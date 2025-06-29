#!/usr/bin/env python3
"""
Quick test to check if blockchain is running and responding
"""

import requests
import json

def test_connection():
    """Test connection to blockchain"""
    print("🔗 Testing Blockchain Connection")
    print("=" * 40)
    
    try:
        # Test /info endpoint
        print("📊 Testing /info endpoint...")
        response = requests.get('http://localhost:5000/info', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Connection successful!")
            print(f"   Blockchain Name: {data.get('name', 'Unknown')}")
            print(f"   Version: {data.get('version', 'Unknown')}")
            print(f"   Total Blocks: {data.get('total_blocks', 0)}")
            print(f"   Chain Valid: {data.get('is_valid', False)}")
            
            # Test dashboard
            print("\n🌐 Testing dashboard...")
            dashboard_response = requests.get('http://localhost:5000/', timeout=5)
            if dashboard_response.status_code == 200:
                print("✅ Dashboard is accessible")
                print("📍 URL: http://localhost:5000")
                
                return True
            else:
                print(f"❌ Dashboard returned status {dashboard_response.status_code}")
                return False
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection refused - blockchain is not running")
        print("💡 Start blockchain with: python blockchain.py")
        return False
    except requests.exceptions.Timeout:
        print("❌ Connection timeout - blockchain may be starting")
        print("💡 Wait a moment and try again")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main test function"""
    if test_connection():
        print("\n🎉 Blockchain is working correctly!")
        print("You can now use:")
        print("   • Enhanced Dashboard: http://localhost:5000")
        print("   • API endpoints for development")
        print("   • All blockchain features")
    else:
        print("\n❌ Blockchain connection failed")
        print("Make sure to run: python blockchain.py")

if __name__ == "__main__":
    main()
