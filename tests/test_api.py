#!/usr/bin/env python3
"""
Quick test to verify Polymarket API connection
"""

import requests
from polymarket_monitor import PolymarketMonitor

def test_api_connection():
    """Test basic API connectivity"""
    print("Testing Polymarket API connection...\n")
    
    monitor = PolymarketMonitor()
    
    # Test 1: Fetch recent trades
    print("1. Fetching recent trades...")
    trades = monitor.get_recent_trades(limit=10)
    
    if trades:
        print(f"   ✓ Successfully fetched {len(trades)} trades")
        
        # Show first trade as example
        if len(trades) > 0:
            first_trade = trades[0]
            value = monitor.calculate_trade_value(first_trade)
            market = first_trade.get('market', {})
            print(f"\n   Example trade:")
            print(f"   - Market: {market.get('title', 'N/A')[:60]}...")
            print(f"   - Value: ${value:,.2f}")
            print(f"   - Side: {first_trade.get('side', 'N/A')}")
            print(f"   - Timestamp: {first_trade.get('timestamp', 'N/A')}")
    else:
        print("   ✗ Failed to fetch trades")
        return False
    
    # Test 2: Check for large trades
    print("\n2. Checking for trades over $5,000 in last 100 trades...")
    trades_100 = monitor.get_recent_trades(limit=100)
    large_trades = [t for t in trades_100 if monitor.calculate_trade_value(t) >= 5000]
    
    print(f"   Found {len(large_trades)} large trades (>${monitor.threshold:,})")
    
    if large_trades:
        print("\n   Recent large trades:")
        for i, trade in enumerate(large_trades[:5], 1):  # Show up to 5
            value = monitor.calculate_trade_value(trade)
            market = trade.get('market', {})
            print(f"   {i}. ${value:,.2f} - {market.get('title', 'Unknown')[:50]}...")
    
    # Test 3: Try to analyze a trader (if we have one)
    if trades and trades[0].get('proxyWallet'):
        wallet = trades[0]['proxyWallet']
        print(f"\n3. Testing trader analysis for wallet: {wallet[:10]}...")
        
        stats = monitor.analyze_trader(wallet)
        print(f"   ✓ Trader has {stats['total_trades']} total trades")
        print(f"   ✓ Total volume: ${stats['total_volume']:,.2f}")
    
    print("\n" + "="*60)
    print("✓ All tests passed! API is working correctly.")
    print("="*60)
    print("\nYou can now run the monitor with: ./run.sh")
    
    return True

if __name__ == "__main__":
    try:
        test_api_connection()
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        print("\nPlease check your internet connection and try again.")

