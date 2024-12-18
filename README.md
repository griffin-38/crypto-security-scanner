# Crypto Token Security Analysis Tool

## Overview

This Python-based tool provides comprehensive security and quality analysis for cryptocurrency tokens, offering multi-layered filtering across various critical dimensions.

## Required APIs

### 1. RugCheck.xyz
- **Purpose**: Contract security analysis
- **Endpoints Needed**:
  * Contract risk assessment
  * Honeypot detection
  * Token verification status
- **Pricing**: Varies (Check website for current pricing)
- **Registration**: https://rugcheck.xyz
- **API Documentation**: Contact RugCheck support

### 2. TweetScout.io
- **Purpose**: Twitter audience analysis
- **Endpoints Needed**:
  * Social media score calculation
  * Follower count
  * Engagement rate analysis
- **Pricing**: 
  * Free tier available
  * Paid plans for advanced features
- **Registration**: https://tweetscout.io
- **API Documentation**: Available in developer portal

### 3. DEXScreener API
- **Purpose**: Token transaction and volume data
- **Endpoints Needed**:
  * Token pair information
  * Transaction volume
  * Liquidity metrics
- **Pricing**: Free
- **Documentation**: https://docs.dexscreener.com

### 4. Rocker Universe API
- **Purpose**: Additional token verification
- **Endpoints Needed**:
  * Token migration tracking
  * Volume verification
- **Pricing**: Varies
- **Registration**: Contact Rocker Universe directly

### 5. Optional APIs
- CoinGecko API (Token metadata)
- Moralis Web3 API (Blockchain data)

### 6. Optional ENV file
- Create .ENV file in your project
- .env file contains placeholders for various API keys
- Includes optional APIs for future expansion
- Adds some basic configuration options

## Command-Line Usage

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/crypto-token-security-tool.git
cd crypto-token-security-tool

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r project-requirements.txt
```

### Configuration

1. Create `.env` file:
```bash
# .env file in project root
RUGCHECK_API_KEY=your_rugcheck_api_key
TWEETSCOUT_API_KEY=your_tweetscout_api_key
DEXSCREENER_API_KEY=your_dexscreener_api_key
ROCKER_UNIVERSE_API_KEY=your_rocker_universe_api_key
```

2. Create `blacklist_config.yaml`:
```bash
# Optional: Customize blacklists
touch blacklist_config.yaml
```

### Running the Tool

#### Basic Usage
```bash
# Run main script
python crypto_security_filter.py

# Analyze specific tokens
python crypto_security_filter.py --tokens 0x123token1 0x456token2

# Export results to CSV
python crypto_security_filter.py --export csv

# Filter by specific criteria
python crypto_security_filter.py --min-volume 5000 --max-age 24
```

#### Advanced Commands
```bash
# Blacklist management
python manage_blacklist.py add-token 0x123suspicious_address
python manage_blacklist.py add-developer 0x456suspicious_dev

# Generate detailed report
python crypto_security_filter.py --report full
```

### Example Workflow

1. Initialize APIs
2. Load token list
3. Run comprehensive analysis
4. Generate security report
5. Export results

```python
# Example Python usage
from crypto_security_filter import CryptoSecurityFilter

# Initialize with API keys
filter = CryptoSecurityFilter(
    rugcheck_key=os.getenv('RUGCHECK_API_KEY'),
    tweetscout_key=os.getenv('TWEETSCOUT_API_KEY')
)

# Analyze tokens
verified_tokens = filter.filter_tokens(token_list)
filter.export_results('security_report.csv')
```

## Troubleshooting

- **API Connection Issues**: 
  * Check API keys
  * Verify network connection
  * Review API documentation

- **Rate Limiting**:
  * Implement exponential backoff
  * Use API key rotation
  * Respect API usage limits

## Performance Tips

- Use asynchronous API calls
- Implement caching
- Batch token processing
- Monitor API response times

## Legal and Ethical Considerations

- This tool is for informational purposes
- Not financial advice
- Users responsible for their own decisions
- Comply with local regulations

## Contributing

1. Fork repository
2. Create feature branch
3. Implement features
4. Submit pull request

## License

