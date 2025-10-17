# Polymarket Trade Monitor - Project Structure

## 📁 Directory Layout

```
polyWarket/
├── 📄 Core Files (root)
│   ├── polymarket_monitor.py      # Main monitoring script
│   ├── example_usage.py            # Usage examples and templates
│   ├── requirements.txt            # Python dependencies
│   ├── .gitignore                 # Git ignore rules
│   └── README.md                  # Landing page (links to docs/)
│
├── 📝 docs/                       # All Documentation
│   ├── README.md                   # Comprehensive documentation
│   ├── QUICKSTART.md              # Quick start guide
│   ├── DOCKER.md                  # Docker deployment guide
│   └── PROJECT_STRUCTURE.md       # This file
│
├── 🐳 docker/                     # Docker Deployment
│   ├── Dockerfile                 # Container image definition
│   ├── docker-compose.yml         # Container orchestration
│   ├── .dockerignore              # Build exclusions
│   └── env.example                # Environment variables template
│
├── 🔧 scripts/                    # Utility Scripts
│   ├── setup.sh                    # One-time environment setup
│   ├── run.sh                     # Quick start script
│   └── docker-test.sh             # Docker setup tester
│
├── 🧪 tests/                      # Test & Debug Scripts
│   ├── README.md                  # Test documentation
│   ├── test_api.py                # API connection test
│   ├── test_fixes.py              # Field extraction test
│   ├── test_no_trades_log.py      # Logging test
│   ├── debug_api.py               # API response inspector
│   └── check_tags.py              # Tags availability checker
│
├── 📊 logs/                       # Generated Logs (gitignored)
│   ├── polymarket_trades.log      # Main log (all trades)
│   ├── tuna_trades.log            # Mid-tier trades ($5K-$100K)
│   ├── whale_trades.log           # High-value trades ($100K+)
│   └── unusual_trades.log         # New/inexperienced traders
│
├── 📦 data/                       # Generated Data (gitignored)
│   ├── trades.json                # Main JSON data (all trades)
│   ├── tuna_trades.json           # Tuna trade data
│   ├── whale_trades.json          # Whale trade data
│   └── unusual_trades.json        # Unusual trader data
│
└── 🐍 venv/                       # Python Virtual Env (gitignored)

```

## 🚀 Quick Start

### Docker (Recommended)

1. **Build and Start**:
   ```bash
   cd docker
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
   ./scripts/setup.sh
   ```

2. **Test** (optional):
   ```bash
   ./venv/bin/python tests/test_api.py
   ```

3. **Run**:
   ```bash
   ./scripts/run.sh
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

### Documentation (`docs/`)

- **`README.md`** - Complete feature documentation
- **`QUICKSTART.md`** - Step-by-step guide
- **`DOCKER.md`** - Docker deployment guide
- **`PROJECT_STRUCTURE.md`** - This overview

### Docker Files (`docker/`)

- **`Dockerfile`** - Container image definition
- **`docker-compose.yml`** - Multi-container orchestration
- **`.dockerignore`** - Files to exclude from image
- **`env.example`** - Environment variable template

### Scripts (`scripts/`)

- **`setup.sh`** - Environment setup (creates venv, installs deps)
- **`run.sh`** - Quick launcher for Python version
- **`docker-test.sh`** - Tests Docker configuration

### Test Scripts (`tests/`)

- **`test_api.py`** - API connection testing
- **`test_fixes.py`** - Field extraction testing
- **`test_no_trades_log.py`** - Logging behavior testing
- **`debug_api.py`** - Raw API inspection
- **`check_tags.py`** - Tag availability checking
- **`README.md`** - Test script documentation

## 🎯 Features

### Trade Detection & Categorization
- ✅ Real-time monitoring (configurable interval)
- ✅ Multi-category trade classification:
  - Main trades: $5,000+ (configurable threshold)
  - Tuna trades: $5K-$100K
  - Whale trades: $100K+
  - Unusual trades: From traders with < 10 previous trades
- ✅ Duplicate detection via transaction hash tracking
- ✅ Logs when no qualifying trades found

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
- ✅ Multi-log system with separate files per category
- ✅ Console output with color/formatting
- ✅ Human-readable logs:
  - `polymarket_trades.log` - Main log (all trades)
  - `tuna_trades.log` - Mid-tier trades
  - `whale_trades.log` - High-value trades
  - `unusual_trades.log` - New/inexperienced traders
- ✅ JSON exports for each category:
  - `trades.json` - All trades
  - `tuna_trades.json` - Tuna trades only
  - `whale_trades.json` - Whale trades only
  - `unusual_trades.json` - Unusual trades only
- ✅ Cross-category logging (trades appear in all applicable logs)
- ✅ Configurable log levels

## 🔧 Configuration

### Docker Deployment

Create a `.env` file from the template:

```bash
cd docker
cp env.example .env
nano .env  # Edit as needed
```

Edit `.env`:
```bash
TRADE_THRESHOLD=5000
POLL_INTERVAL=30
```

Then start:
```bash
docker-compose up -d
```

### Python Deployment

Set environment variables or run directly:

```bash
export TRADE_THRESHOLD=5000
export POLL_INTERVAL=30
python polymarket_monitor.py

# Or use the helper script
./scripts/run.sh
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
TRADE DETECTED: $7,500.00 [TUNA]
================================================================================
Trade Details:
  - Market: Will Trump win the 2024 Presidential Election?
  - Market ID: 0xe3b423dfad8c22ff75c9899c4e8176f628cf4ad4...
  - Category: US-current-affairs
  - Username: crypto_trader_pro (Mighty-Whale)
  - Total Historical Trades: 247
  ...
```

**Example with multiple categories:**
```
================================================================================
TRADE DETECTED: $125,000.00 [WHALE + UNUSUAL]
================================================================================
...
```

### JSON Output
```json
{
  "timestamp": "2025-10-17T18:15:30.123456",
  "categories": {
    "is_unusual": false,
    "is_tuna": true,
    "is_whale": false
  },
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

