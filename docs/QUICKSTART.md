# Quick Start Guide

## Setup (Choose One)

### Option 1: Docker (Easiest)

```bash
# From project root
cd docker
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

See [DOCKER.md](DOCKER.md) for more details.

### Option 2: Python Virtual Environment

```bash
./scripts/setup.sh
```

## Test the Connection (Non-Docker)

```bash
./venv/bin/python tests/test_api.py
```

## Run the Monitor

### Docker:
```bash
cd docker
docker-compose up -d
docker-compose logs -f
```

### Python:
```bash
./scripts/run.sh
```

That's it! The monitor will:
1. Check for new trades every 30 seconds
2. Categorize and log trades to multiple files based on size and trader experience:
   - **Main Log**: All trades over $5,000 → `polymarket_trades.log` / `trades.json`
   - **Tuna Trades**: $5K-$100K → `tuna_trades.log` / `tuna_trades.json`
   - **Whale Trades**: $100K+ → `whale_trades.log` / `whale_trades.json`
   - **Unusual Trades**: From traders with < 10 previous trades → `unusual_trades.log` / `unusual_trades.json`
3. For each qualifying trade, automatically analyze the trader's complete history
4. Display market details including category and tags
5. Log when no qualifying trades are found in each polling cycle

**Note**: A single trade can appear in multiple logs (e.g., a $150K trade from a new trader appears in main, whale, and unusual logs)

## What You'll See

### Trade Detected (Tuna Category):

```
================================================================================
TRADE DETECTED: $7,500.00 [TUNA]
================================================================================
Trade Details:
  - Transaction Hash: 0xabc123...
  - Market: Will Trump win the 2024 Presidential Election?
  - Market ID: 0xe3b423dfad8c22ff75c9899c4e8176f628cf4ad4...
  - Category: US-current-affairs
  - Tags: politics, election, 2024
  - Outcome: Yes
  - Side: BUY
  - Size: 10000 tokens
  - Price: $0.75

Trader Information:
  - Wallet: 0x1234567890abcdef...
  - Username: crypto_trader_pro (Mighty-Whale)
  - Total Historical Trades: 247
  - Total Volume Traded: $456,789.50
  - Markets Traded: 42
================================================================================
```

### Trade Detected (Whale + Unusual):

```
================================================================================
TRADE DETECTED: $125,000.00 [WHALE + UNUSUAL]
================================================================================
Trader Information:
  - Total Historical Trades: 8
  - ...
================================================================================
```

### No Qualifying Trades:

```
2025-10-17 18:15:30,123 - INFO - No transactions over $5,000.00 found in this batch
```

## Customization

Edit `polymarket_monitor.py` (around line 355):

```python
monitor = PolymarketMonitor(
    threshold=5000,      # Change threshold (e.g., 10000 for $10k)
    poll_interval=30     # Change frequency (e.g., 15 for every 15 seconds)
)
```

## Stop Monitoring

Press `Ctrl+C`

## View Logs

**Main Logs** (all trades):
- Human-readable: `cat logs/polymarket_trades.log`
- JSON format: `cat data/trades.json`

**Category-Specific Logs**:
- Tuna trades: `cat logs/tuna_trades.log` or `cat data/tuna_trades.json`
- Whale trades: `cat logs/whale_trades.log` or `cat data/whale_trades.json`
- Unusual traders: `cat logs/unusual_trades.log` or `cat data/unusual_trades.json`

## Need Help?

See [README.md](README.md) for detailed documentation or [DOCKER.md](DOCKER.md) for Docker-specific help.

