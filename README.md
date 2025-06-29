# Production Blockchain Prototype

A functional blockchain implementation using Python Flask, designed as a prototype for a production-level blockchain system.

## Features

### Core Blockchain Features
- **Blocks**: Immutable blocks with transactions, timestamps, and proof-of-work
- **Transactions**: Secure transfer of value between addresses
- **Mining**: Proof-of-Work consensus mechanism with configurable difficulty
- **Wallet System**: Balance tracking and transaction validation
- **Chain Validation**: Cryptographic integrity verification

### Network Features
- **Distributed Nodes**: Multi-node network support
- **Consensus Algorithm**: Longest valid chain resolution
- **REST API**: Complete HTTP API for blockchain operations
- **Thread Safety**: Concurrent mining protection

### Production-Ready Elements
- **Error Handling**: Comprehensive validation and error responses
- **Security**: Hash-based integrity and transaction validation
- **Scalability**: Modular design for easy extension
- **Documentation**: Well-documented codebase

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup
1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Start the blockchain node:**
```bash
python blockchain.py
```

3. **Start on custom port (optional):**
```bash
python blockchain.py -p 5001
```

## Usage

### Running the Blockchain
```bash
# Start main node
python blockchain.py

# Start additional nodes for testing
python blockchain.py -p 5001
python blockchain.py -p 5002
```

### Testing the System
```bash
# Run comprehensive test suite
python test_blockchain.py
```

## API Endpoints

### Blockchain Operations
- `GET /chain` - View the complete blockchain
- `GET /info` - Get blockchain information
- `GET /validate` - Validate blockchain integrity

### Transaction Operations
- `POST /transactions/new` - Create a new transaction
- `GET /mine` - Mine pending transactions
- `GET /balance/<address>` - Get wallet balance
- `GET /wallets` - View all wallet balances

### Network Operations
- `POST /nodes/register` - Register network nodes
- `GET /nodes/resolve` - Run consensus algorithm

## API Examples

### Create a Transaction
```bash
curl -X POST http://localhost:5000/transactions/new \
  -H "Content-Type: application/json" \
  -d '{"sender": "alice", "recipient": "bob", "amount": 50}'
```

### Mine Transactions
```bash
curl http://localhost:5000/mine
```

### Check Balance
```bash
curl http://localhost:5000/balance/alice
```

### View Blockchain
```bash
curl http://localhost:5000/chain
```

### Register Network Node
```bash
curl -X POST http://localhost:5000/nodes/register \
  -H "Content-Type: application/json" \
  -d '{"nodes": ["localhost:5001", "localhost:5002"]}'
```

### Run Consensus
```bash
curl http://localhost:5000/nodes/resolve
```

## Architecture

### Core Components

#### Transaction Class
- Handles individual transactions
- Cryptographic hashing
- Validation logic
- Serialization

#### Block Class
- Contains multiple transactions
- Proof-of-Work mining
- Chain linking via previous hash
- Immutable structure

#### Blockchain Class
- Manages the complete chain
- Transaction pool
- Mining rewards
- Consensus mechanism
- Network node management

### Security Features
- **SHA-256 Hashing**: Cryptographic integrity
- **Proof-of-Work**: Mining difficulty adjustment
- **Balance Validation**: Prevents double spending
- **Chain Validation**: Detects tampering attempts

### Network Architecture
- **REST API**: HTTP-based communication
- **Multi-Node Support**: Distributed network
- **Consensus**: Longest valid chain wins
- **Thread Safety**: Concurrent operation protection

## Configuration

### Blockchain Parameters
- **Difficulty**: Mining difficulty (default: 4)
- **Mining Reward**: Block reward (default: 10)
- **Genesis Supply**: Initial coin supply (default: 1,000,000)

### Network Settings
- **Default Port**: 5000
- **Host**: 0.0.0.0 (all interfaces)
- **Debug Mode**: Enabled for development

## Testing

### Automated Tests
The `test_blockchain.py` script provides comprehensive testing:
- Transaction creation and validation
- Mining operations
- Balance tracking
- Chain integrity
- Error handling

### Manual Testing
Use curl, Postman, or any HTTP client to interact with the API endpoints.

## Production Considerations

### Current Limitations
- In-memory storage (no persistence)
- Simple wallet system
- Basic network protocol
- Limited scalability features

### Production Enhancements Needed
- **Database Storage**: Persistent blockchain storage
- **Advanced Consensus**: More sophisticated algorithms
- **Smart Contracts**: Programmable transactions
- **Performance Optimization**: Faster mining and validation
- **Security Hardening**: Advanced cryptographic features
- **Monitoring**: Comprehensive logging and metrics

### Scalability Improvements
- **Sharding**: Horizontal scaling
- **Layer 2 Solutions**: Off-chain transactions
- **Optimized Data Structures**: Merkle trees
- **Caching**: Performance optimization

## Development

### Code Structure
```
blockchain.py       # Main blockchain implementation
test_blockchain.py  # Comprehensive test suite
requirements.txt    # Python dependencies
README.md          # Documentation
```

### Key Classes
- `Transaction`: Individual transaction handling
- `Block`: Block creation and mining
- `Blockchain`: Complete blockchain management
- Flask Routes: REST API endpoints

### Extension Points
- Custom consensus algorithms
- Additional transaction types
- Enhanced validation rules
- Network protocol improvements

## License

This is a prototype implementation for educational and development purposes.

## Contributing

This blockchain prototype serves as a foundation for production development. Key areas for contribution:
- Performance optimization
- Security enhancements
- Additional features
- Documentation improvements

## Support

For questions about this blockchain prototype, please refer to the code documentation and test examples.
