# Changelog

## [Reorganization] - 2025-10-16

### 🎯 Major Restructuring

The project has been reorganized for better manageability and clarity.

### 📁 Directory Changes

**Before:**
```
polyWarket/
├── polymarket_monitor.py
├── example_usage.py
├── requirements.txt
├── README.md                    # 5 markdown files at root
├── QUICKSTART.md
├── DOCKER.md
├── PROJECT_STRUCTURE.md
├── REORGANIZATION_PLAN.md
├── Dockerfile                   # Docker files scattered
├── docker-compose.yml
├── .dockerignore
├── env.example
├── setup.sh                     # Scripts scattered
├── run.sh
├── docker-test.sh
├── tests/
├── logs/
└── data/
```

**After:**
```
polyWarket/
├── polymarket_monitor.py        # Core files at root
├── example_usage.py
├── requirements.txt
├── .gitignore
├── README.md                    # Single landing page
│
├── docs/                        # All documentation organized
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── DOCKER.md
│   └── PROJECT_STRUCTURE.md
│
├── docker/                      # Docker files grouped
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .dockerignore
│   └── env.example
│
├── scripts/                     # Utility scripts grouped
│   ├── setup.sh
│   ├── run.sh
│   └── docker-test.sh
│
├── tests/                       # Tests (unchanged)
├── logs/                        # Runtime (unchanged)
└── data/                        # Runtime (unchanged)
```

### ✨ Benefits

1. **Better Organization**: Related files are grouped together
2. **Cleaner Root**: Only 5 items at root instead of 13+
3. **Easier Navigation**: Clear separation of docs, docker, and scripts
4. **Scalable**: Easy to add more files without cluttering root
5. **Professional**: Industry-standard project structure

### 🔄 Updated Commands

**Setup:**
- Old: `./setup.sh`
- New: `./scripts/setup.sh`

**Run:**
- Old: `./run.sh`
- New: `./scripts/run.sh`

**Docker:**
- Old: `docker-compose up -d`
- New: `cd docker && docker-compose up -d` (or `docker-compose -f docker/docker-compose.yml up -d`)

**Documentation:**
- Old: `cat README.md`
- New: `cat docs/README.md` (root README.md is now a landing page)

### 📝 Updated Files

All documentation and scripts have been updated to reflect the new structure:

- ✅ `README.md` - New landing page at root
- ✅ `docs/README.md` - Updated with new paths
- ✅ `docs/QUICKSTART.md` - Updated command examples
- ✅ `docs/DOCKER.md` - Updated Docker workflow
- ✅ `docs/PROJECT_STRUCTURE.md` - Reflects new organization
- ✅ `scripts/setup.sh` - Updated to work from scripts/ directory
- ✅ `scripts/run.sh` - Updated to work from scripts/ directory
- ✅ `scripts/docker-test.sh` - Updated for new docker/ location
- ✅ `docker/docker-compose.yml` - Updated build context and volumes
- ✅ `.gitignore` - Added docker/.env

### 🧪 Compatibility

- All existing functionality remains unchanged
- Scripts automatically detect and navigate to project root
- Docker volumes point to correct locations
- No code changes to core monitoring script

### 📚 Documentation

See `REORGANIZATION_PLAN.md` for detailed rationale and migration notes.

---

## [Multi-Category Trade Tracking] - 2025-10-17

### 🎯 Enhanced Trade Categorization System

Implemented a comprehensive multi-category trade tracking system with separate logs and data files for different trade types.

### 📊 New Trade Categories

**1. Main Trades Log** (`polymarket_trades.log` / `trades.json`)
- Logs ALL trades that meet any criteria ($5,000+)
- Central log for all qualifying trades
- Replaces previous "large trades" terminology

**2. Unusual Trades** (`unusual_trades.log` / `unusual_trades.json`)
- Trades from wallets with < 10 previous trades
- Identifies new or inexperienced traders making significant moves
- Also logged in main log and appropriate size category (tuna/whale)

**3. Tuna Trades** (`tuna_trades.log` / `tuna_trades.json`)
- Trades between $5,000 and $100,000
- Mid-tier significant trades
- Also logged in main log

**4. Whale Trades** (`whale_trades.log` / `whale_trades.json`)
- Trades $100,000 and above
- High-value, market-moving trades
- Also logged in main log

### ✨ Key Features

- **Multi-Log System**: Each trade is logged to multiple files based on its characteristics
- **Category Labels**: Log entries clearly show trade categories (e.g., `[WHALE + UNUSUAL]`)
- **Separate JSON Files**: Independent data files for each category for easy analysis
- **Automatic Directory Creation**: Logs and data directories created automatically
- **Enhanced Startup Info**: Monitor displays all thresholds on startup

### 🔧 Technical Changes

- Renamed `log_large_trade()` → `log_trade()`
- Added separate loggers for each category (unusual, tuna, whale)
- Updated terminology from "Large Trade" to "Trade"
- Added `categories` field to JSON output with boolean flags
- Added configurable thresholds via environment variables:
  - `TUNA_MIN` (default: 5000)
  - `TUNA_MAX` (default: 100000)
  - `WHALE_MIN` (default: 100000)
  - `UNUSUAL_TRADER_THRESHOLD` (default: 10)
- Updated `docker/env.example` with new configuration options

### 📁 New Files Created

**Log Files** (in `logs/` or `/app/logs`):
- `polymarket_trades.log` - Main log
- `unusual_trades.log` - Unusual trader activity
- `tuna_trades.log` - Mid-tier trades
- `whale_trades.log` - High-value trades

**Data Files** (in `data/` or `/app/data`):
- `trades.json` - Main data
- `unusual_trades.json` - Unusual trader data
- `tuna_trades.json` - Tuna trade data
- `whale_trades.json` - Whale trade data

### 📝 Example Output

```
================================================================================
TRADE DETECTED: $125,000.00 [WHALE + UNUSUAL]
================================================================================
Trade Details:
  - Transaction Hash: 0x...
  - Market: Will Donald Trump win the 2024 election?
  - Total Historical Trades: 8
  - ...
```

---

## Previous Updates

### [Initial Release]

- Real-time trade monitoring
- Trader history analysis
- Market category and tags
- JSON and text logging
- Docker support
- Environment-based configuration
