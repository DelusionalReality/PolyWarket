# Polymarket Trade Monitor - Project Structure

## 📁 Directory Layout

```
polyWarket/
├── 📄 Core Files
│   ├── polymarket_monitor.py      # Main monitoring script
│   ├── example_usage.py            # Usage examples and templates
│   ├── run.sh                      # Quick start script
│   └── setup.sh                    # One-time setup script
│
├── 📝 Documentation
│   ├── README.md                   # Comprehensive documentation
│   ├── QUICKSTART.md              # Quick start guide
│   ├── DOCKER.md                  # Docker deployment guide
│   └── PROJECT_STRUCTURE.md       # This file
│
├── 🔧 Configuration
│   ├── requirements.txt            # Python dependencies
│   ├── .gitignore                 # Git ignore rules
│   ├── Dockerfile                 # Docker image definition
│   ├── docker-compose.yml         # Docker Compose configuration
│   ├── .dockerignore              # Docker build exclusions
│   └── env.example                # Environment variables template
│
├── 🧪 Tests & Debug (tests/)
│   ├── README.md                  # Test documentation
│   ├── test_api.py                # API connection test
│   ├── test_fixes.py              # Field extraction test
│   ├── test_no_trades_log.py      # Logging test
│   ├── debug_api.py               # API response inspector
│   └── check_tags.py              # Tags availability checker
│
├── 📊 Generated Files (gitignored)
│   ├── polymarket_trades.log      # Human-readable logs
│   ├── large_trades.json          # JSON formatted data
│   └── venv/                      # Python virtual environment
│
└── 🗂️ Runtime
    └── __pycache__/               # Python cache files

```

## 🚀 Quick Start

### Docker (Recommended)

1. **Build and Start**:
   ```bash
   docker-compose up -d
   ```

2. **View Logs**:
   ```bash
   docker-compose logs -f
   ```

3. **Stop**:
   ```bash
   docker-compose down
   ```

### Python Virtual Environment

1. **Setup** (one time):
   ```bash
   ./setup.sh
   ```

2. **Test** (optional):
   ```bash
   ./venv/bin/python tests/test_api.py
   ```

3. **Run**:
   ```bash
   ./run.sh
   ```

## 📚 File Descriptions

### Core Scripts

- **`polymarket_monitor.py`** - Main monitoring application
  - Monitors trades in real-time (30-second intervals)
  - Logs trades over $5,000
  - Analyzes trader history
  - Fetches market categories and tags
  - Exports to JSON and log files

- **`example_usage.py`** - Example configurations
  - Basic monitoring
  - High threshold monitoring
  - One-time scans
  - Trader analysis examples

### Helper Scripts

- **`run.sh`** - Convenience launcher
  - Auto-creates venv if missing
  - Runs monitor with proper environment

- **`setup.sh`** - Installation script
  - Creates virtual environment
  - Installs dependencies
  - Sets up execution permissions

### Test Scripts (`tests/`)

All test and debug scripts have been organized into the `tests/` directory:

- **`test_api.py`** - Validates API connectivity
- **`test_fixes.py`** - Verifies correct field extraction
- **`test_no_trades_log.py`** - Tests logging behavior
- **`debug_api.py`** - Inspects raw API responses
- **`check_tags.py`** - Checks tag availability

### Documentation

- **`README.md`** - Complete feature documentation
- **`QUICKSTART.md`** - Step-by-step guide
- **`DOCKER.md`** - Docker deployment guide
- **`tests/README.md`** - Test script documentation
- **`PROJECT_STRUCTURE.md`** - This overview

### Docker Files

- **`Dockerfile`** - Container image definition
- **`docker-compose.yml`** - Multi-container orchestration
- **`.dockerignore`** - Files to exclude from image
- **`env.example`** - Environment variable template

## 🎯 Features

### Trade Detection
- ✅ Real-time monitoring (configurable interval)
- ✅ Threshold-based filtering ($5,000 default)
- ✅ Duplicate detection via transaction hash tracking
- ✅ Logs when no large trades found

### Market Information
- ✅ Market title and description
- ✅ Market ID (condition ID)
- ✅ Market category (e.g., "US-current-affairs")
- ✅ Market tags (when available)
- ✅ Market slug and event slug

### Trader Analysis
- ✅ Username and pseudonym
- ✅ Complete trade history count
- ✅ Total volume traded
- ✅ Number of markets traded
- ✅ First and latest trade timestamps

### Logging & Output
- ✅ Console output with color/formatting
- ✅ File logging (`polymarket_trades.log`)
- ✅ JSON export (`large_trades.json`)
- ✅ Configurable log levels

## 🔧 Configuration

### Docker Deployment

Create a `.env` file from the template:

```bash
cp env.example .env
```

Edit `.env`:
```bash
TRADE_THRESHOLD=5000
POLL_INTERVAL=30
```

### Python Deployment

Edit `polymarket_monitor.py` or set environment variables:

```bash
export TRADE_THRESHOLD=5000
export POLL_INTERVAL=30
python polymarket_monitor.py
```

## 📡 APIs Used

1. **Trade Data API**
   - Endpoint: `https://data-api.polymarket.com/trades`
   - Provides: Trade data, usernames, market titles

2. **Market Details API**
   - Endpoint: `https://gamma-api.polymarket.com/markets`
   - Provides: Market categories, tags, metadata
   - Cached to minimize API calls

## 📊 Output Format

### Console/Log Output
```
================================================================================
LARGE TRADE DETECTED: $7,500.00
================================================================================
Trade Details:
  - Market: Will Trump win the 2024 Presidential Election?
  - Market ID: 0xe3b423dfad8c22ff75c9899c4e8176f628cf4ad4...
  - Category: US-current-affairs
  - Username: crypto_trader_pro (Mighty-Whale)
  - Total Historical Trades: 247
  ...
```

### JSON Output
```json
{
  "timestamp": "2025-10-16T18:15:30.123456",
  "trade": {
    "value": 7500.00,
    "market_title": "Will Trump win...",
    "market_category": "US-current-affairs",
    "market_tags": ["politics", "election"]
  },
  "trader": {
    "username": "crypto_trader_pro",
    "total_trades": 247
  }
}
```

## 🛠️ Development

To add new features:

1. Modify `polymarket_monitor.py`
2. Add tests to `tests/` directory
3. Update documentation in `README.md`
4. Test with `./venv/bin/python tests/test_api.py`

## 📝 Notes

- Virtual environment isolates dependencies
- All test scripts moved to `tests/` for organization
- Market details are cached for performance
- Timestamps use Unix epoch format

