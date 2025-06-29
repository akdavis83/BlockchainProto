#!/usr/bin/env python3
"""
Simple manual test for blockchain functionality
Tests basic operations without Flask server
"""

import sys
import os

def test_basic_blockchain():
    """Test basic blockchain functionality"""
    print("🧪 Testing Basic Blockchain Functionality")
    print("=" * 50)
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        # Import blockchain components
        print("📦 Importing blockchain components...")
        from blockchain import Transaction, Block, Blockchain
        print("✅ Import successful")
        
        # Create blockchain
        print("\n🔗 Creating blockchain...")
        bc = Blockchain()
        print(f"✅ Blockchain created with {len(bc.chain)} blocks")
        
        # Check genesis block
        genesis = bc.chain[0]
        print(f"✅ Genesis block hash: {genesis.hash[:16]}...")
        
        # Create transaction
        print("\n💸 Creating transaction...")
        tx = Transaction("genesis", "alice", 100)
        print(f"✅ Transaction created: {tx.sender} → {tx.recipient} ({tx.amount} coins)")
        
        # Add transaction
        if bc.add_transaction(tx):
            print("✅ Transaction added to pending pool")
        else:
            print("❌ Failed to add transaction")
            return False
        
        # Check pending transactions
        print(f"✅ Pending transactions: {len(bc.pending_transactions)}")
        
        # Mine block
        print("\n⛏️ Mining block...")
        block = bc.mine_pending_transactions("miner")
        print(f"✅ Block mined! Hash: {block.hash[:16]}...")
        print(f"✅ Blockchain now has {len(bc.chain)} blocks")
        
        # Check balances
        print("\n💰 Checking balances...")
        alice_balance = bc.get_balance("alice")
        miner_balance = bc.get_balance("miner")
        print(f"✅ Alice balance: {alice_balance} coins")
        print(f"✅ Miner balance: {miner_balance} coins")
        
        # Validate chain
        print("\n🔍 Validating blockchain...")
        is_valid = bc.is_chain_valid()
        print(f"✅ Blockchain valid: {is_valid}")
        
        if is_valid:
            print("\n🎉 ALL TESTS PASSED! Blockchain is working correctly.")
            return True
        else:
            print("\n❌ Blockchain validation failed")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure blockchain.py is in the current directory")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_flask_import():
    """Test Flask import separately"""
    print("\n🌐 Testing Flask Import")
    print("=" * 30)
    
    try:
        import flask
        print(f"✅ Flask version: {flask.__version__}")
        
        import requests
        print(f"✅ Requests version: {requests.__version__}")
        
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Run: pip install flask requests")
        return False

def main():
    """Run all tests"""
    print("🔬 BLOCKCHAIN SIMPLE TEST SUITE")
    print("This tests blockchain functionality without starting the server")
    print()
    
    # Test Flask import
    flask_ok = test_flask_import()
    
    # Test basic blockchain
    blockchain_ok = test_basic_blockchain()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    print(f"Flask/Requests: {'✅ PASS' if flask_ok else '❌ FAIL'}")
    print(f"Blockchain Core: {'✅ PASS' if blockchain_ok else '❌ FAIL'}")
    
    if flask_ok and blockchain_ok:
        print("\n🎉 Core functionality works! The issue is likely with:")
        print("   • Port conflicts")
        print("   • Firewall blocking")
        print("   • Permission issues")
        print("\n💡 Try running the diagnostic script:")
        print("   python diagnose_blockchain.py")
    else:
        print("\n❌ Core functionality issues detected.")
        print("   Fix the import/dependency issues first.")

if __name__ == "__main__":
    main()
