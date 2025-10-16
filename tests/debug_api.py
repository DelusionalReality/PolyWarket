#!/usr/bin/env python3
"""
Debug script to inspect the actual API response structure
"""

import requests
import json

def inspect_api_response():
    """Fetch and display raw API response to understand structure"""
    
    print("Fetching trade data from Polymarket API...\n")
    
    # Fetch trades
    url = "https://data-api.polymarket.com/trades"
    params = {'limit': 5}
    
    response = requests.get(url, params=params)
    trades = response.json()
    
    if trades:
        print(f"Received {len(trades)} trades\n")
        print("="*80)
        print("FIRST TRADE - FULL STRUCTURE:")
        print("="*80)
        print(json.dumps(trades[0], indent=2))
        
        print("\n" + "="*80)
        print("KEY FIELDS SUMMARY:")
        print("="*80)
        
        for i, trade in enumerate(trades[:3], 1):
            print(f"\nTrade {i}:")
            print(f"  Transaction Hash: {trade.get('transactionHash', 'N/A')}")
            print(f"  Size: {trade.get('size', 'N/A')}")
            print(f"  Price: {trade.get('price', 'N/A')}")
            print(f"  Side: {trade.get('side', 'N/A')}")
            print(f"  Outcome: {trade.get('outcome', 'N/A')}")
            print(f"  Timestamp: {trade.get('timestamp', 'N/A')}")
            print(f"  Proxy Wallet: {trade.get('proxyWallet', 'N/A')}")
            
            # Check market field structure
            if 'market' in trade:
                print(f"  Market (type): {type(trade['market'])}")
                print(f"  Market keys: {list(trade['market'].keys()) if isinstance(trade['market'], dict) else 'N/A'}")
            
            # Check user field structure
            if 'user' in trade:
                print(f"  User (type): {type(trade['user'])}")
                print(f"  User keys: {list(trade['user'].keys()) if isinstance(trade['user'], dict) else 'N/A'}")
    
    print("\n" + "="*80)
    
    # Also test fetching market details separately
    print("\nTesting market details endpoint...")
    
    # Try to get a market ID from a trade
    if trades and 'market' in trades[0]:
        market_data = trades[0]['market']
        print(f"Market data type: {type(market_data)}")
        print(f"Market data: {market_data}")
        
        # If market is just an ID string, try fetching market details
        if isinstance(market_data, str):
            print(f"\nFetching market details for ID: {market_data}")
            market_url = f"https://data-api.polymarket.com/markets/{market_data}"
            market_response = requests.get(market_url)
            if market_response.status_code == 200:
                market_info = market_response.json()
                print(json.dumps(market_info, indent=2))
    
    print("\n" + "="*80)
    print("Testing user history endpoint...")
    
    if trades and trades[0].get('proxyWallet'):
        wallet = trades[0]['proxyWallet']
        print(f"Fetching trades for wallet: {wallet}")
        
        user_url = "https://data-api.polymarket.com/trades"
        user_params = {'user': wallet, 'limit': 5}
        user_response = requests.get(user_url, params=user_params)
        
        if user_response.status_code == 200:
            user_trades = user_response.json()
            print(f"Found {len(user_trades)} trades for this user")
            if user_trades:
                print("\nFirst trade structure:")
                print(json.dumps(user_trades[0], indent=2)[:1000] + "...")

if __name__ == "__main__":
    inspect_api_response()

