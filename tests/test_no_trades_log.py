#!/usr/bin/env python3
"""
Test that the monitor logs when no large trades are found
"""

from polymarket_monitor import PolymarketMonitor
import time

def test_no_trades_log():
    """Test the new log message for when no large trades are found"""
    
    print("Testing 'no large trades' log message...\n")
    
    # Create monitor with very high threshold to ensure no trades qualify
    monitor = PolymarketMonitor(threshold=1000000)  # $1 million threshold
    
    print(f"Monitor threshold set to: ${monitor.threshold:,.2f}")
    print(f"Fetching trades...\n")
    
    # Fetch recent trades
    trades = monitor.get_recent_trades(limit=100)
    
    print(f"Processing {len(trades)} trades...")
    print("Expected: Log message saying 'No transactions over $1,000,000.00 found'\n")
    print("-" * 80)
    
    # Process trades - should find none over $1M
    monitor.process_trades(trades)
    
    print("-" * 80)
    print("\n✓ Test complete!")
    print("\nNow testing with normal threshold ($5,000)...\n")
    
    # Test with normal threshold
    monitor2 = PolymarketMonitor(threshold=5000)
    print(f"Monitor threshold set to: ${monitor2.threshold:,.2f}")
    print(f"Processing {len(trades)} trades...")
    print("-" * 80)
    
    monitor2.process_trades(trades)
    
    print("-" * 80)
    print("\n✓ All tests complete!")

if __name__ == "__main__":
    test_no_trades_log()

