#!/usr/bin/env python3
"""
Test the fixed monitor to ensure market names and usernames display correctly
"""

from polymarket_monitor import PolymarketMonitor

def test_fixes():
    """Test that market names and usernames are correctly displayed"""
    
    print("Testing updated monitor with correct field names...\n")
    
    monitor = PolymarketMonitor(threshold=1000)  # Lower threshold for testing
    
    # Fetch recent trades
    print("1. Fetching recent trades...")
    trades = monitor.get_recent_trades(limit=20)
    
    if not trades:
        print("   No trades found!")
        return
    
    print(f"   ✓ Found {len(trades)} trades\n")
    
    # Check first few trades for proper field extraction
    print("2. Checking field extraction from first 3 trades:")
    for i, trade in enumerate(trades[:3], 1):
        market_title = trade.get('title', 'Unknown')
        username = trade.get('name', 'Anonymous')
        pseudonym = trade.get('pseudonym', '')
        condition_id = trade.get('conditionId', 'N/A')
        
        print(f"\n   Trade {i}:")
        print(f"     Market: {market_title}")
        print(f"     Condition ID: {condition_id[:20]}...")
        print(f"     Username: {username}")
        print(f"     Pseudonym: {pseudonym}")
        print(f"     Value: ${monitor.calculate_trade_value(trade):,.2f}")
    
    # Test market details lookup
    print("\n3. Testing market category lookup...")
    if trades and trades[0].get('conditionId'):
        condition_id = trades[0]['conditionId']
        market_details = monitor.get_market_details(condition_id)
        
        if market_details:
            print(f"   ✓ Market category: {market_details.get('category', 'N/A')}")
            print(f"   ✓ Question: {market_details.get('question', 'N/A')[:60]}...")
        else:
            print("   ⚠ Could not fetch market details (might be a new market)")
    
    # Test trader analysis
    print("\n4. Testing trader analysis...")
    if trades and trades[0].get('proxyWallet'):
        wallet = trades[0]['proxyWallet']
        stats = monitor.analyze_trader(wallet)
        
        print(f"   Wallet: {wallet}")
        print(f"   ✓ Username: {stats.get('username', 'N/A')}")
        print(f"   ✓ Pseudonym: {stats.get('pseudonym', 'N/A')}")
        print(f"   ✓ Total trades: {stats['total_trades']}")
        print(f"   ✓ Markets traded: {stats['markets_traded']}")
    
    # Find and log one large trade if available
    print("\n5. Looking for a trade over $1,000 to test logging...")
    large_trades = [t for t in trades if monitor.calculate_trade_value(t) >= 1000]
    
    if large_trades:
        print(f"   Found {len(large_trades)} trades over $1,000")
        print(f"   Testing log format with first large trade...\n")
        
        trade = large_trades[0]
        wallet = trade.get('proxyWallet')
        if wallet:
            stats = monitor.analyze_trader(wallet)
            monitor.log_large_trade(trade, stats)
    else:
        print("   No trades over $1,000 in this batch")
    
    print("\n" + "="*80)
    print("✓ All tests completed!")
    print("="*80)
    print("\nIf you see actual market names and usernames above (not 'Unknown'),")
    print("then the fixes are working correctly!")

if __name__ == "__main__":
    test_fixes()

