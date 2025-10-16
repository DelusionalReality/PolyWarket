# Test and Debug Scripts

This directory contains test and debug scripts for the Polymarket Trade Monitor.

## Test Scripts

### test_api.py
Tests the basic API connection and functionality.

**Usage:**
```bash
../venv/bin/python test_api.py
```

**What it does:**
- Fetches recent trades from Polymarket API
- Displays example trade data
- Checks for large trades
- Tests trader analysis functionality

### test_fixes.py
Tests that market names and usernames are correctly extracted from the API.

**Usage:**
```bash
../venv/bin/python test_fixes.py
```

**What it does:**
- Verifies market titles are displayed (not "Unknown")
- Verifies usernames and pseudonyms are displayed
- Tests market category lookup
- Tests trader analysis with real data

### test_no_trades_log.py
Tests the "no large trades found" logging functionality.

**Usage:**
```bash
../venv/bin/python test_no_trades_log.py
```

**What it does:**
- Tests logging when no trades exceed the threshold
- Verifies the message format

## Debug Scripts

### debug_api.py
Inspects the raw API response structure to understand the data format.

**Usage:**
```bash
../venv/bin/python debug_api.py
```

**What it does:**
- Displays full trade structure from API
- Shows all available fields
- Helps debug API response changes

### check_tags.py
Checks if market tags are available in the Polymarket APIs.

**Usage:**
```bash
../venv/bin/python check_tags.py
```

**What it does:**
- Examines trade and market API responses
- Looks for tags and category fields
- Tests different API endpoints

## Running Tests

From the project root directory:

```bash
# Test basic API connection
./venv/bin/python tests/test_api.py

# Test field extraction
./venv/bin/python tests/test_fixes.py

# Debug API responses
./venv/bin/python tests/debug_api.py
```

Or from within the tests directory:

```bash
cd tests
../venv/bin/python test_api.py
```

