# Quick Start Guide

## Setup (Choose One)

### Option 1: Docker (Easiest)

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

See [DOCKER.md](DOCKER.md) for more details.

### Option 2: Python Virtual Environment

```bash
./setup.sh
```

## Test the Connection (Non-Docker)

```bash
./venv/bin/python tests/test_api.py
```

## Run the Monitor

### Docker:
```bash
docker-compose up -d
docker-compose logs -f
```

### Python:
```bash
./run.sh
```

That's it! The monitor will:
1. Check for new trades every 30 seconds
2. Log any trade over $5,000 to console and `polymarket_trades.log`
3. For each large trade, automatically analyze the trader's complete history
4. Display market details including category and tags
5. Save all data to `large_trades.json` for further analysis
6. Log when no large trades are found in each polling cycle

## What You'll See

### Large Trade Detected:

```
================================================================================
LARGE TRADE DETECTED: $7,500.00
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

### No Large Trades:

```
2025-10-16 18:15:30,123 - INFO - No transactions over $5,000.00 found in this batch
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

- **Human-readable**: `cat polymarket_trades.log`
- **JSON format**: `cat large_trades.json`

## Need Help?

See `README.md` for detailed documentation.

