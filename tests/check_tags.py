#!/usr/bin/env python3
"""Check if tags are available in the API"""

import requests
import json

# Get a recent trade
response = requests.get("https://data-api.polymarket.com/trades", params={'limit': 1})
trades = response.json()

if trades:
    trade = trades[0]
    print("Trade keys:")
    print(json.dumps(list(trade.keys()), indent=2))
    
    # Check if there's a market endpoint we can query
    condition_id = trade.get('conditionId')
    slug = trade.get('slug')
    
    print(f"\nCondition ID: {condition_id}")
    print(f"Slug: {slug}")
    
    # Try to get market details
    if slug:
        print(f"\nTrying to fetch market details for slug: {slug}")
        market_url = f"https://data-api.polymarket.com/markets/{slug}"
        market_response = requests.get(market_url)
        
        if market_response.status_code == 200:
            market_data = market_response.json()
            print("\nMarket data keys:")
            print(json.dumps(list(market_data.keys()), indent=2))
            
            if 'tags' in market_data:
                print(f"\nTags found: {market_data['tags']}")
            else:
                print("\nNo 'tags' field in market data")
                
            print("\nFull market response (first 2000 chars):")
            print(json.dumps(market_data, indent=2)[:2000])
        else:
            print(f"Market API returned status {market_response.status_code}")

