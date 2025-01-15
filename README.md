# Crypto Token Security Tool

A comprehensive security analysis tool for cryptocurrency tokens that integrates with multiple APIs to detect potential risks, scams, and suspicious patterns.

## Features

- Multi-API token analysis integration (RugCheck, TweetScout, DEXScreener, Rocker Universe)
- Volume legitimacy verification
- Contract security analysis
- Blacklist management for suspicious tokens and developers
- Comprehensive logging and monitoring
- Async API integration for improved performance
- Configurable security thresholds and parameters

## Prerequisites

- Python 3.9+
- pip
- Virtual environment (recommended)
- API keys for supported services

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crypto-security.git
cd crypto-security
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
# For development
pip install -r requirements-dev.txt

# For production
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configurations
```

## Usage

Basic usage example:

```python
from crypto_security import CryptoSecurityFilter
import asyncio

async def analyze_tokens():
    # Initialize the security filter
    security_filter = CryptoSecurityFilter(
        rugcheck_api_key='your_key',
        rocker_universe_api_key='your_key'
    )
    
    # Token data to analyze
    tokens = [
        {
            'address': '0x123token_address',
            'symbol': 'TOKEN1',
            'volume': 5000,
            'volume_1h': 500,
            'volume_24h': 10000,
            'developer_address': '0x456dev_address'
        }
    ]
    
    # Analyze tokens
    results = await security_filter.analyze_tokens(tokens)
    
    # Process results
    for token in results:
        print(f"Token: {token['symbol']}")
        print(f"Risk Level: {token.get('risk_level')}")
        print(f"Security Score: {token.get('security_score')}")
        print("---")

# Run the analysis
asyncio.run(analyze_tokens())
```

## API Integration

The tool supports the following APIs:

1. RugCheck.xyz
   - Contract analysis
   - Honeypot detection
   - Risk assessment

2. TweetScout.io
   - Social media analysis
   - Community metrics
   - Trend detection

3. DEXScreener
   - Market data
   - Trading volume analysis
   - Liquidity tracking

4. Rocker Universe
   - Additional market metrics
   - Token analytics
   - Historical data

## Configuration

See `ENV.md` for detailed configuration options and environment variables.

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=crypto_security tests/

# Run specific test file
pytest tests/test_security_filter.py
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Acknowledgments

- RugCheck.xyz API
- TweetScout.io API
- DEXScreener API
- Rocker Universe API

## License

This project is licensed under the MIT License - see the LICENSE file for details.
