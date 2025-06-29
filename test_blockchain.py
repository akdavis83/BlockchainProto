#!/usr/bin/env python3
"""
Test script for the blockchain prototype
Demonstrates key functionality of the blockchain
"""

import requests
import json
import time

# Base URL for the blockchain API
BASE_URL = "http://localhost:5000"

def make_request(method, endpoint, data=None):
    """Helper function to make HTTP requests"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        return response.json(), response.status_code
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to blockchain node. Make sure it's running on port 5000.")
        return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def print_response(response, status_code):
    """Pretty print API response"""
    if response is None:
        return
    
    print(f"Status Code: {status_code}")
    print(f"Response: {json.dumps(response, indent=2)}")
    print("-" * 50)

def test_blockchain():
    """Test the blockchain functionality"""
    print("🔗 Testing Blockchain Prototype")
    print("=" * 50)
    
    # 1. Check blockchain info
    print("1. Getting blockchain info...")
    response, status = make_request("GET", "/info")
    print_response(response, status)
    
    # 2. View initial chain
    print("2. Viewing initial blockchain...")
    response, status = make_request("GET", "/chain")
    print_response(response, status)
    
    # 3. Check wallet balances
    print("3. Checking initial wallet balances...")
    response, status = make_request("GET", "/wallets")
    print_response(response, status)
    
    # 4. Create some transactions
    print("4. Creating transactions...")
    
    # Transaction 1: Genesis sends to Alice
    tx1 = {
        "sender": "genesis",
        "recipient": "alice",
        "amount": 100
    }
    response, status = make_request("POST", "/transactions/new", tx1)
    print("Transaction 1 (Genesis -> Alice):")
    print_response(response, status)
    
    # Transaction 2: Genesis sends to Bob
    tx2 = {
        "sender": "genesis",
        "recipient": "bob",
        "amount": 50
    }
    response, status = make_request("POST", "/transactions/new", tx2)
    print("Transaction 2 (Genesis -> Bob):")
    print_response(response, status)
    
    # 5. Mine the transactions
    print("5. Mining pending transactions...")
    response, status = make_request("GET", "/mine")
    print_response(response, status)
    
    # 6. Check updated balances
    print("6. Checking updated wallet balances...")
    response, status = make_request("GET", "/wallets")
    print_response(response, status)
    
    # 7. Create more transactions
    print("7. Creating more transactions...")
    
    # Alice sends to Bob
    tx3 = {
        "sender": "alice",
        "recipient": "bob",
        "amount": 25
    }
    response, status = make_request("POST", "/transactions/new", tx3)
    print("Transaction 3 (Alice -> Bob):")
    print_response(response, status)
    
    # Bob sends to Charlie
    tx4 = {
        "sender": "bob",
        "recipient": "charlie",
        "amount": 30
    }
    response, status = make_request("POST", "/transactions/new", tx4)
    print("Transaction 4 (Bob -> Charlie):")
    print_response(response, status)
    
    # 8. Mine again
    print("8. Mining second batch of transactions...")
    response, status = make_request("GET", "/mine")
    print_response(response, status)
    
    # 9. Check final balances
    print("9. Checking final wallet balances...")
    response, status = make_request("GET", "/wallets")
    print_response(response, status)
    
    # 10. View final blockchain
    print("10. Viewing final blockchain...")
    response, status = make_request("GET", "/chain")
    print_response(response, status)
    
    # 11. Validate the blockchain
    print("11. Validating blockchain integrity...")
    response, status = make_request("GET", "/validate")
    print_response(response, status)
    
    # 12. Test insufficient balance scenario
    print("12. Testing insufficient balance scenario...")
    tx_invalid = {
        "sender": "alice",
        "recipient": "bob",
        "amount": 1000  # Alice doesn't have this much
    }
    response, status = make_request("POST", "/transactions/new", tx_invalid)
    print("Invalid transaction (insufficient balance):")
    print_response(response, status)

def test_individual_balances():
    """Test individual balance queries"""
    print("\n💰 Testing Individual Balance Queries")
    print("=" * 50)
    
    addresses = ["genesis", "alice", "bob", "charlie", "miner"]
    
    for address in addresses:
        response, status = make_request("GET", f"/balance/{address}")
        print(f"Balance for {address}:")
        print_response(response, status)

if __name__ == "__main__":
    print("🚀 Blockchain Test Suite")
    print("Make sure the blockchain node is running: python blockchain.py")
    print()
    
    # Wait a moment for user to read
    time.sleep(2)
    
    # Run tests
    test_blockchain()
    test_individual_balances()
    
    print("\n✅ Test suite completed!")
    print("You can also test the API manually using curl or Postman with the following endpoints:")
    print("- GET  http://localhost:5000/chain")
    print("- POST http://localhost:5000/transactions/new")
    print("- GET  http://localhost:5000/mine")
    print("- GET  http://localhost:5000/balance/<address>")
    print("- GET  http://localhost:5000/validate")
    print("- GET  http://localhost:5000/info")
    print("- GET  http://localhost:5000/wallets")
