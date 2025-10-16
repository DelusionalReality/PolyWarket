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

## Previous Updates

### [Initial Release]

- Real-time trade monitoring
- Trader history analysis
- Market category and tags
- JSON and text logging
- Docker support
- Environment-based configuration

