# 🚀 START HERE

Welcome to the Polymarket Trade Monitor!

## ✨ Project Reorganization Complete

This project has been reorganized for better manageability. Everything is working and ready to use!

## 📁 New Structure

```
polyWarket/
├── 📄 Core Files (root)
│   ├── polymarket_monitor.py  ← Main script
│   ├── example_usage.py
│   ├── requirements.txt
│   └── README.md              ← Landing page
│
├── 📝 docs/                   ← All documentation
│   ├── README.md              ← Full feature docs
│   ├── QUICKSTART.md          ← Quick start guide
│   ├── DOCKER.md              ← Docker deployment
│   └── PROJECT_STRUCTURE.md   ← Project details
│
├── 🐳 docker/                 ← Docker files
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── env.example
│
├── 🔧 scripts/                ← Utility scripts
│   ├── setup.sh               ← Run this first!
│   ├── run.sh
│   └── docker-test.sh
│
└── 🧪 tests/                  ← Test scripts
```

## 🎯 Quick Start (Choose One)

### Option 1: Docker (Easiest)

```bash
cd docker
docker-compose up -d
docker-compose logs -f
```

### Option 2: Python

```bash
./scripts/setup.sh     # One-time setup
./scripts/run.sh       # Start monitoring
```

## 📚 Documentation Guide

| Document | Purpose | Location |
|----------|---------|----------|
| **Landing Page** | Quick overview & links | `README.md` |
| **Full Documentation** | Complete features & setup | `docs/README.md` |
| **Quick Start** | Get running fast | `docs/QUICKSTART.md` |
| **Docker Guide** | Docker deployment | `docs/DOCKER.md` |
| **Project Structure** | Detailed organization | `docs/PROJECT_STRUCTURE.md` |
| **Migration Guide** | Update from old structure | `MIGRATION_GUIDE.md` |
| **Changelog** | What changed | `CHANGELOG.md` |
| **Summary** | Reorganization summary | `SUMMARY.md` |

## 🎓 What to Read First

1. **First time?** Start with `README.md` (this is a landing page)
2. **Want to get running?** Read `docs/QUICKSTART.md`
3. **Using Docker?** See `docs/DOCKER.md`
4. **Need details?** Check `docs/README.md`

## 💡 Most Common Commands

```bash
# Setup (one time)
./scripts/setup.sh

# Run monitor
./scripts/run.sh

# Docker
cd docker && docker-compose up -d

# View logs
tail -f logs/polymarket_trades.log

# View JSON data
cat data/large_trades.json

# Test API
./venv/bin/python tests/test_api.py
```

## 📝 Key Features

- ✅ Monitors trades over $5,000 (configurable)
- ✅ Analyzes complete trader history
- ✅ Shows market categories and tags
- ✅ Exports to logs and JSON
- ✅ Docker support
- ✅ Runs continuously (30-second polling)

## 🔍 Example Output

```
================================================================================
LARGE TRADE DETECTED: $9,635.60
================================================================================
Trade Details:
  - Market: Ethereum Up or Down - October 16, 2:15PM-2:30PM ET
  - Category: crypto
  - Username: aespaning2 (Idle-Exaggeration)
  
Trader Information:
  - Total Historical Trades: 500
  - Total Volume Traded: $7,760.99
  - Markets Traded: 6
================================================================================
```

## ❓ Need Help?

- **Quick questions?** See `docs/QUICKSTART.md`
- **Docker issues?** See `docs/DOCKER.md`
- **Full documentation?** See `docs/README.md`
- **Migrating from old structure?** See `MIGRATION_GUIDE.md`

## 🎉 You're All Set!

Just run:

```bash
./scripts/setup.sh && ./scripts/run.sh
```

Or with Docker:

```bash
cd docker && docker-compose up -d
```

---

**Next Steps:** Read `docs/QUICKSTART.md` or just run `./scripts/setup.sh`!

