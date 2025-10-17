# Polymarket Trade Monitor

A Python script that monitors and categorizes significant trades on Polymarket, with separate tracking for whale trades, tuna trades, and unusual trader activity.

## Features

- 🔍 **Real-time Monitoring**: Continuously monitors Polymarket for new trades (default: every 30 seconds)
- 💰 **Multi-Category Trade Detection**: 
  - **Main Trades**: All trades over $5,000 (configurable threshold)
  - **Tuna Trades**: Mid-tier trades between $5,000 and $100,000
  - **Whale Trades**: High-value trades over $100,000
  - **Unusual Trades**: Trades from wallets with < 10 previous trades
- 📊 **Detailed Market Information**: 
  - Market title and description
  - Market ID (condition ID) for tracking
  - Market category (e.g., "US-current-affairs", "crypto")
  - Market tags (when available)
  - Market slug and event slug for URL construction
- 👤 **Trader Analysis**: For each qualifying trade, automatically analyzes the complete trader history:
  - Username and pseudonym
  - Total number of historical trades on Polymarket
  - Total volume traded across all markets
  - Number of unique markets traded
  - First and latest trade timestamps
- 📝 **Comprehensive Multi-Log System**: 
  - Human-readable logs to console and separate category files
  - Machine-readable JSON output for each category
  - Automatic cross-logging to multiple categories when applicable

## Installation

### Option 1: Docker (Recommended for Production)

The easiest way to deploy:

```bash
# From project root
cd docker
docker-compose up -d

# View logs
docker-compose logs -f
```

See [DOCKER.md](DOCKER.md) for complete Docker documentation.

### Option 2: Python Virtual Environment

Run the setup script which will create a virtual environment and install dependencies:

```bash
./scripts/setup.sh
```

### Option 3: Manual Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the virtual environment:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the monitor with default settings ($5,000 threshold, 30-second polling):

**Option 1: Easiest - Use the run script**
```bash
# From project root
./scripts/run.sh
```

**Option 2: Using the virtual environment directly**
```bash
./venv/bin/python polymarket_monitor.py
```

**Option 3: Activate virtual environment first**
```bash
source venv/bin/activate
python polymarket_monitor.py
```

**Option 4: Docker**
```bash
cd docker
docker-compose up -d
```

### Testing

Test the API connection before running the monitor:

```bash
./venv/bin/python tests/test_api.py
```

All test and debug scripts are located in the `tests/` directory.

### Advanced Usage

You can customize the monitor by editing the script's `main()` function:

```python
monitor = PolymarketMonitor(
    threshold=10000,     # Monitor trades over $10,000
    poll_interval=30     # Check every 30 seconds
)
```

### Output Files

The monitor creates separate log and data files for each trade category:

**Log Files** (in `logs/` directory):
- `polymarket_trades.log` - Main log containing all qualifying trades
- `tuna_trades.log` - Mid-tier trades ($5K-$100K)
- `whale_trades.log` - High-value trades ($100K+)
- `unusual_trades.log` - Trades from inexperienced traders (< 10 previous trades)

**Data Files** (in `data/` directory):
- `trades.json` - JSON-formatted log of all trades
- `tuna_trades.json` - JSON data for tuna trades
- `whale_trades.json` - JSON data for whale trades
- `unusual_trades.json` - JSON data for unusual trader activity

**Note**: Trades can appear in multiple logs. For example, a $150,000 trade from a wallet with 5 previous trades will be logged in:
- `polymarket_trades.log` (main log)
- `whale_trades.log` (value category)
- `unusual_trades.log` (trader experience category)

## Example Output

### When a trade is detected:

**Example 1: Whale Trade from Experienced Trader**
```
================================================================================
TRADE DETECTED: $125,000.00 [WHALE]
================================================================================
Trade Details:
  - Transaction Hash: 0xabc123...
  - Market: Will Trump win the 2024 Presidential Election?
  - Market ID: 0xe3b423dfad8c22ff75c9899c4e8176f628cf4ad4caa00481764d320e7415f7a9
  - Market Slug: trump-2024-presidential-election
  - Event Slug: trump-2024-presidential-election
  - Category: US-current-affairs
  - Tags: politics, election, 2024
  - Outcome: Yes
  - Side: BUY
  - Size: 166667 tokens
  - Price: $0.75
  - Timestamp: 1729123456

Trader Information:
  - Wallet: 0x1234567890abcdef...
  - Username: crypto_trader_pro (Mighty-Whale)
  - Total Historical Trades: 247
  - Total Volume Traded: $1,456,789.50
  - Markets Traded: 42
  - First Trade: 1724567890
  - Latest Trade: 1729123456
================================================================================
```

**Example 2: Tuna Trade from New Trader**
```
================================================================================
TRADE DETECTED: $8,500.00 [TUNA + UNUSUAL]
================================================================================
Trade Details:
  - Transaction Hash: 0xdef456...
  - Market: Bitcoin to reach $100k by end of 2024?
  - Category: crypto
  - ...

Trader Information:
  - Wallet: 0xabcdefgh...
  - Username: newbie_trader
  - Total Historical Trades: 6
  - Total Volume Traded: $24,500.00
  - Markets Traded: 3
  - ...
================================================================================
```

### When no qualifying trades are found:

```
2025-10-17 18:15:30,123 - INFO - No transactions over $5,000.00 found in this batch
```

## API Information

This script uses the Polymarket public APIs:
- **Trade Data API**: `https://data-api.polymarket.com/trades`
  - Fetches real-time trade information
  - Includes trader usernames and market titles
- **Market Details API**: `https://gamma-api.polymarket.com/markets`
  - Fetches market categories and additional metadata
  - Cached to minimize API calls

## Configuration

Key parameters you can adjust via environment variables:

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `TRADE_THRESHOLD` | 5000 | Minimum trade value in USD to log |
| `POLL_INTERVAL` | 30 | Seconds between API checks |
| `TUNA_MIN` | 5000 | Minimum value for tuna trade classification |
| `TUNA_MAX` | 100000 | Maximum value for tuna trade classification (exclusive) |
| `WHALE_MIN` | 100000 | Minimum value for whale trade classification |
| `UNUSUAL_TRADER_THRESHOLD` | 10 | Maximum previous trades for unusual classification |

**Docker Setup:**
Copy `docker/env.example` to `docker/.env` and adjust values as needed.

**Non-Docker Setup:**
Export environment variables before running:
```bash
export TUNA_MIN=10000
export WHALE_MIN=200000
./scripts/run.sh
```

## Notes

- **Multi-Category Logging**: Trades are automatically logged to all applicable categories (e.g., a $150K trade from a new trader appears in main, whale, and unusual logs)
- The script maintains a set of seen transaction hashes to avoid duplicate logging within categories
- API requests are rate-limited by the polling interval
- Trade value is calculated as `size × price` where size is in tokens and price is the token price
- Market details are cached to reduce API calls and improve performance
- Timestamps are in Unix epoch format (seconds since January 1, 1970)
- Directories for logs and data are created automatically if they don't exist

## Stopping the Monitor

Press `Ctrl+C` to gracefully stop the monitoring script.

## Troubleshooting

**No trades appearing?**
- Check your internet connection
- Verify the Polymarket API is accessible
- Consider lowering the threshold or increasing the limit of trades fetched

**API errors?**
- The script will log errors and continue running
- Check the log file for detailed error messages

## 📄 License

Open source - feel free to use and modify.

## 🔗 Resources

- [Polymarket](https://polymarket.com/)
- [Polymarket API Documentation](https://docs.polymarket.com/)
- [Docker Documentation](https://docs.docker.com/)