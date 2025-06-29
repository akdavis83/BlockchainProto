import hashlib
import json
import time
from urllib.parse import urlparse
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
import threading


class Transaction:
    """Represents a transaction in the blockchain"""
    
    def __init__(self, sender, recipient, amount, timestamp=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp or time.time()
        self.transaction_id = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate hash of the transaction"""
        transaction_string = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"
        return hashlib.sha256(transaction_string.encode()).hexdigest()
    
    def to_dict(self):
        """Convert transaction to dictionary"""
        return {
            'transaction_id': self.transaction_id,
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
    
    def is_valid(self):
        """Validate transaction"""
        if self.amount <= 0:
            return False
        if self.sender == self.recipient:
            return False
        return True


class Block:
    """Represents a block in the blockchain"""
    
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate hash of the block"""
        block_string = json.dumps({
            'index': self.index,
            'transactions': [tx.to_dict() if hasattr(tx, 'to_dict') else tx for tx in self.transactions],
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        """Mine the block using Proof of Work"""
        target = "0" * difficulty
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        print(f"Block mined: {self.hash}")
        return self.hash
    
    def to_dict(self):
        """Convert block to dictionary"""
        return {
            'index': self.index,
            'transactions': [tx.to_dict() if hasattr(tx, 'to_dict') else tx for tx in self.transactions],
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }


class Blockchain:
    """Main blockchain class"""
    
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.mining_reward = 10
        self.nodes = set()
        
        # Wallet balances (in production, this would be calculated from the chain)
        self.balances = {
            'genesis': 1000000,  # Genesis wallet with initial supply
            'miner': 0
        }
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_transaction = Transaction("genesis", "genesis", 0, time.time())
        return Block(0, [genesis_transaction], time.time(), "0")
    
    def get_latest_block(self):
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_transaction(self, transaction):
        """Add a new transaction to pending transactions"""
        if not isinstance(transaction, Transaction):
            return False
        
        if not transaction.is_valid():
            return False
        
        # Check if sender has sufficient balance
        if transaction.sender != 'genesis' and self.get_balance(transaction.sender) < transaction.amount:
            return False
        
        self.pending_transactions.append(transaction)
        return True
    
    def mine_pending_transactions(self, mining_reward_address):
        """Mine pending transactions and create a new block"""
        # Add mining reward transaction
        reward_transaction = Transaction(None, mining_reward_address, self.mining_reward, time.time())
        self.pending_transactions.append(reward_transaction)
        
        # Create new block
        block = Block(
            len(self.chain),
            self.pending_transactions,
            time.time(),
            self.get_latest_block().hash
        )
        
        # Mine the block
        block.mine_block(self.difficulty)
        
        # Add block to chain
        self.chain.append(block)
        
        # Update balances
        self.update_balances(block)
        
        # Clear pending transactions
        self.pending_transactions = []
        
        return block
    
    def update_balances(self, block):
        """Update wallet balances based on block transactions"""
        for transaction in block.transactions:
            if hasattr(transaction, 'sender') and hasattr(transaction, 'recipient'):
                sender = transaction.sender
                recipient = transaction.recipient
                amount = transaction.amount
                
                # Deduct from sender (except for mining rewards)
                if sender and sender != 'genesis':
                    if sender not in self.balances:
                        self.balances[sender] = 0
                    self.balances[sender] -= amount
                
                # Add to recipient
                if recipient not in self.balances:
                    self.balances[recipient] = 0
                self.balances[recipient] += amount
    
    def get_balance(self, address):
        """Get balance for a specific address"""
        return self.balances.get(address, 0)
    
    def is_chain_valid(self):
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block hash is valid
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if current block points to previous block
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Check proof of work
            if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                return False
        
        return True
    
    def register_node(self, address):
        """Register a new node in the network"""
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    def resolve_conflicts(self):
        """Consensus algorithm - replace chain with longest valid chain"""
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)
        
        for node in neighbours:
            try:
                response = requests.get(f'http://{node}/chain')
                if response.status_code == 200:
                    data = response.json()
                    length = data['length']
                    chain_data = data['chain']
                    
                    # Check if chain is longer and valid
                    if length > max_length:
                        # Convert dict back to blockchain objects for validation
                        temp_blockchain = Blockchain()
                        temp_blockchain.chain = []
                        
                        for block_data in chain_data:
                            transactions = []
                            for tx_data in block_data['transactions']:
                                tx = Transaction(
                                    tx_data['sender'],
                                    tx_data['recipient'],
                                    tx_data['amount'],
                                    tx_data['timestamp']
                                )
                                transactions.append(tx)
                            
                            block = Block(
                                block_data['index'],
                                transactions,
                                block_data['timestamp'],
                                block_data['previous_hash'],
                                block_data['nonce']
                            )
                            block.hash = block_data['hash']
                            temp_blockchain.chain.append(block)
                        
                        if temp_blockchain.is_chain_valid():
                            max_length = length
                            new_chain = temp_blockchain.chain
            except requests.RequestException:
                continue
        
        if new_chain:
            self.chain = new_chain
            return True
        
        return False
    
    def to_dict(self):
        """Convert blockchain to dictionary"""
        return {
            'chain': [block.to_dict() for block in self.chain],
            'length': len(self.chain),
            'difficulty': self.difficulty,
            'pending_transactions': [tx.to_dict() for tx in self.pending_transactions],
            'balances': self.balances
        }


# Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
blockchain = Blockchain()

# Thread lock for mining
mining_lock = threading.Lock()


@app.route('/chain', methods=['GET'])
def full_chain():
    """Get the full blockchain"""
    response = {
        'chain': [block.to_dict() for block in blockchain.chain],
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """Create a new transaction"""
    values = request.get_json()
    
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    try:
        amount = float(values['amount'])
        transaction = Transaction(values['sender'], values['recipient'], amount)
        
        if blockchain.add_transaction(transaction):
            response = {'message': f'Transaction will be added to next block'}
            return jsonify(response), 201
        else:
            return jsonify({'message': 'Invalid transaction or insufficient balance'}), 400
    except ValueError:
        return jsonify({'message': 'Invalid amount'}), 400


@app.route('/mine', methods=['GET'])
def mine():
    """Mine a new block"""
    with mining_lock:
        if not blockchain.pending_transactions:
            return jsonify({'message': 'No transactions to mine'}), 400
        
        # Mine the block
        block = blockchain.mine_pending_transactions('miner')
        
        response = {
            'message': 'New block forged',
            'index': block.index,
            'transactions': [tx.to_dict() for tx in block.transactions],
            'hash': block.hash,
            'previous_hash': block.previous_hash,
            'nonce': block.nonce
        }
        return jsonify(response), 200


@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    """Get balance for an address"""
    balance = blockchain.get_balance(address)
    return jsonify({'address': address, 'balance': balance}), 200


@app.route('/validate', methods=['GET'])
def validate_chain():
    """Validate the blockchain"""
    is_valid = blockchain.is_chain_valid()
    return jsonify({'valid': is_valid}), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    """Register new nodes"""
    values = request.get_json()
    nodes = values.get('nodes')
    
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
    
    for node in nodes:
        blockchain.register_node(node)
    
    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    """Consensus algorithm"""
    replaced = blockchain.resolve_conflicts()
    
    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': [block.to_dict() for block in blockchain.chain]
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': [block.to_dict() for block in blockchain.chain]
        }
    
    return jsonify(response), 200


@app.route('/info', methods=['GET'])
def blockchain_info():
    """Get blockchain information"""
    response = {
        'name': 'Production Blockchain Prototype',
        'version': '1.0.0',
        'total_blocks': len(blockchain.chain),
        'difficulty': blockchain.difficulty,
        'pending_transactions': len(blockchain.pending_transactions),
        'mining_reward': blockchain.mining_reward,
        'total_nodes': len(blockchain.nodes),
        'is_valid': blockchain.is_chain_valid()
    }
    return jsonify(response), 200


@app.route('/wallets', methods=['GET'])
def get_wallets():
    """Get all wallet balances"""
    return jsonify({'wallets': blockchain.balances}), 200


@app.route('/', methods=['GET'])
@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Serve the enhanced blockchain dashboard"""
    try:
        with open('enhanced_blockchain_dashboard.html', 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        # Fallback to original dashboard
        try:
            with open('blockchain_dashboard.html', 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except FileNotFoundError:
            return jsonify({
                'error': 'Dashboard not found', 
                'message': 'Please ensure enhanced_blockchain_dashboard.html is in the same directory'
            }), 404


if __name__ == '__main__':
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    
    print(f"Starting blockchain node on port {port}")
    print("Available endpoints:")
    print("  GET  /chain - View the blockchain")
    print("  POST /transactions/new - Create a new transaction")
    print("  GET  /mine - Mine pending transactions")
    print("  GET  /balance/<address> - Get wallet balance")
    print("  GET  /validate - Validate the blockchain")
    print("  POST /nodes/register - Register network nodes")
    print("  GET  /nodes/resolve - Consensus mechanism")
    print("  GET  /info - Blockchain information")
    print("  GET  /wallets - View all wallet balances")
    
    app.run(host='0.0.0.0', port=port, debug=True)
