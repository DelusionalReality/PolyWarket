#!/usr/bin/env python3
"""
Polymarket Trade Monitor
Monitors large trades (>$5000) on Polymarket and analyzes trader history
"""

import requests
import time
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Configure logging
# Check if running in Docker (data directory exists)
log_file = '/app/logs/polymarket_trades.log' if os.path.exists('/app/logs') else 'polymarket_trades.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class PolymarketMonitor:
    """Monitor and analyze Polymarket trades"""
    
    BASE_URL = "https://data-api.polymarket.com"
    GAMMA_API_URL = "https://gamma-api.polymarket.com"
    TRADE_THRESHOLD = 5000  # USD threshold for logging trades
    
    def __init__(self, threshold: float = 5000, poll_interval: int = 30):
        """
        Initialize the monitor
        
        Args:
            threshold: Minimum trade size in USD to log (default: 5000)
            poll_interval: Seconds between API polls (default: 30)
        """
        self.threshold = threshold
        self.poll_interval = poll_interval
        self.seen_transactions = set()
        self.market_cache = {}  # Cache market details by condition ID
        
    def get_recent_trades(self, limit: int = 100) -> List[Dict]:
        """
        Fetch recent trades from Polymarket
        
        Args:
            limit: Number of trades to fetch (max 10000)
            
        Returns:
            List of trade dictionaries
        """
        url = f"{self.BASE_URL}/trades"
        params = {
            'limit': limit,
            'offset': 0
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching trades: {e}")
            return []
    
    def get_user_trade_history(self, wallet_address: str) -> List[Dict]:
        """
        Get all trades for a specific wallet address
        
        Args:
            wallet_address: The user's proxy wallet address
            
        Returns:
            List of all trades by this user
        """
        url = f"{self.BASE_URL}/trades"
        params = {
            'user': wallet_address,
            'limit': 10000  # Get maximum possible trades
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching user history for {wallet_address}: {e}")
            return []
    
    def get_market_details(self, condition_id: str) -> Optional[Dict]:
        """
        Get market details including category/tags from Gamma API
        
        Args:
            condition_id: The market condition ID
            
        Returns:
            Market details dictionary or None if not found
        """
        # Check cache first
        if condition_id in self.market_cache:
            return self.market_cache[condition_id]
        
        url = f"{self.GAMMA_API_URL}/markets"
        params = {
            'id': condition_id,
            'limit': 1
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            markets = response.json()
            
            if markets and len(markets) > 0:
                market_details = markets[0]
                # Cache the result
                self.market_cache[condition_id] = market_details
                return market_details
            
            return None
        except requests.exceptions.RequestException as e:
            logger.debug(f"Could not fetch market details for {condition_id}: {e}")
            return None
    
    def calculate_trade_value(self, trade: Dict) -> float:
        """
        Calculate the USD value of a trade
        
        Args:
            trade: Trade dictionary from API
            
        Returns:
            Trade value in USD
        """
        # size is in tokens, price is per token (typically in USDC)
        size = float(trade.get('size', 0))
        price = float(trade.get('price', 0))
        
        # For SELL orders, calculate based on (1 - price) for the opposite outcome
        # But for value calculation, we use the actual amount traded
        return size * price
    
    def analyze_trader(self, wallet_address: str) -> Dict:
        """
        Analyze a trader's history
        
        Args:
            wallet_address: The user's proxy wallet address
            
        Returns:
            Dictionary with trader statistics
        """
        trades = self.get_user_trade_history(wallet_address)
        
        if not trades:
            return {
                'wallet': wallet_address,
                'total_trades': 0,
                'total_volume': 0,
                'markets_traded': 0
            }
        
        total_volume = sum(self.calculate_trade_value(t) for t in trades)
        # conditionId is the unique market identifier
        unique_markets = set(t.get('conditionId', '') for t in trades if t.get('conditionId'))
        
        # Get user info from first trade (fields are at top level)
        username = trades[0].get('name', 'Anonymous')
        pseudonym = trades[0].get('pseudonym', '')
        
        return {
            'wallet': wallet_address,
            'username': username,
            'pseudonym': pseudonym,
            'total_trades': len(trades),
            'total_volume': round(total_volume, 2),
            'markets_traded': len(unique_markets),
            'first_trade': trades[-1].get('timestamp', 'Unknown') if trades else 'Unknown',
            'latest_trade': trades[0].get('timestamp', 'Unknown') if trades else 'Unknown'
        }
    
    def log_large_trade(self, trade: Dict, trader_stats: Dict):
        """
        Log details about a large trade and trader history
        
        Args:
            trade: Trade dictionary
            trader_stats: Trader statistics dictionary
        """
        trade_value = self.calculate_trade_value(trade)
        
        # Extract fields from top-level trade object
        market_title = trade.get('title', 'Unknown Market')
        market_id = trade.get('conditionId', 'N/A')
        market_slug = trade.get('slug', 'N/A')
        event_slug = trade.get('eventSlug', 'N/A')
        
        # Try to get market category/tags from Gamma API
        market_category = 'N/A'
        market_tags = []
        
        if market_id and market_id != 'N/A':
            market_details = self.get_market_details(market_id)
            if market_details:
                market_category = market_details.get('category', 'N/A')
                # Some markets might have a tags field
                if 'tags' in market_details:
                    market_tags = market_details.get('tags', [])
        
        # Build trader display name
        username = trader_stats.get('username', 'Anonymous')
        pseudonym = trader_stats.get('pseudonym', '')
        trader_display = f"{username} ({pseudonym})" if pseudonym else username
        
        # Build tags display
        tags_display = ', '.join(market_tags) if market_tags else 'None'
        
        log_message = f"""
{'='*80}
LARGE TRADE DETECTED: ${trade_value:,.2f}
{'='*80}
Trade Details:
  - Transaction Hash: {trade.get('transactionHash', 'N/A')}
  - Market: {market_title}
  - Market ID: {market_id}
  - Market Slug: {market_slug}
  - Event Slug: {event_slug}
  - Category: {market_category}
  - Tags: {tags_display}
  - Outcome: {trade.get('outcome', 'N/A')}
  - Side: {trade.get('side', 'N/A')}
  - Size: {trade.get('size', 0)} tokens
  - Price: ${trade.get('price', 0)}
  - Timestamp: {trade.get('timestamp', 'N/A')}

Trader Information:
  - Wallet: {trader_stats['wallet']}
  - Username: {trader_display}
  - Total Historical Trades: {trader_stats['total_trades']}
  - Total Volume Traded: ${trader_stats['total_volume']:,.2f}
  - Markets Traded: {trader_stats['markets_traded']}
  - First Trade: {trader_stats.get('first_trade', 'N/A')}
  - Latest Trade: {trader_stats.get('latest_trade', 'N/A')}
{'='*80}
        """
        
        logger.info(log_message)
        
        # Also save to JSON for easier parsing
        trade_data = {
            'timestamp': datetime.now().isoformat(),
            'trade': {
                'value': trade_value,
                'transaction_hash': trade.get('transactionHash'),
                'market_title': market_title,
                'market_id': market_id,
                'market_slug': market_slug,
                'event_slug': event_slug,
                'market_category': market_category,
                'market_tags': market_tags,
                'outcome': trade.get('outcome'),
                'side': trade.get('side'),
                'size': trade.get('size'),
                'price': trade.get('price'),
                'trade_timestamp': trade.get('timestamp'),
                'icon': trade.get('icon')
            },
            'trader': trader_stats
        }
        
        # Append to JSON log file
        # Use data directory if running in Docker
        json_file = '/app/data/large_trades.json' if os.path.exists('/app/data') else 'large_trades.json'
        
        try:
            with open(json_file, 'a') as f:
                f.write(json.dumps(trade_data) + '\n')
        except Exception as e:
            logger.error(f"Error writing to JSON log: {e}")
    
    def process_trades(self, trades: List[Dict]):
        """
        Process a list of trades, filtering for large ones
        
        Args:
            trades: List of trade dictionaries
        """
        large_trades_found = 0
        
        for trade in trades:
            tx_hash = trade.get('transactionHash')
            
            # Skip if we've already processed this transaction
            if tx_hash in self.seen_transactions:
                continue
            
            self.seen_transactions.add(tx_hash)
            trade_value = self.calculate_trade_value(trade)
            
            # Check if trade exceeds threshold
            if trade_value >= self.threshold:
                large_trades_found += 1
                wallet = trade.get('proxyWallet')
                if wallet:
                    logger.info(f"Found large trade: ${trade_value:,.2f} from wallet {wallet}")
                    
                    # Analyze trader history
                    trader_stats = self.analyze_trader(wallet)
                    
                    # Log the trade and trader info
                    self.log_large_trade(trade, trader_stats)
        
        # Log if no large trades were found
        if large_trades_found == 0:
            logger.info(f"No transactions over ${self.threshold:,.2f} found in this batch")
    
    def run(self):
        """
        Main monitoring loop
        """
        logger.info(f"Starting Polymarket monitor (threshold: ${self.threshold:,.2f})")
        logger.info(f"Poll interval: {self.poll_interval} seconds")
        logger.info("Press Ctrl+C to stop")
        
        try:
            while True:
                logger.debug("Fetching recent trades...")
                trades = self.get_recent_trades()
                
                if trades:
                    logger.debug(f"Processing {len(trades)} trades")
                    self.process_trades(trades)
                else:
                    logger.warning("No trades received")
                
                time.sleep(self.poll_interval)
                
        except KeyboardInterrupt:
            logger.info("\nMonitoring stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)


def main():
    """Main entry point"""
    # Support environment variables for Docker deployment
    threshold = float(os.getenv('TRADE_THRESHOLD', '5000'))
    poll_interval = int(os.getenv('POLL_INTERVAL', '30'))
    
    # Create monitor with settings from environment or defaults
    monitor = PolymarketMonitor(
        threshold=threshold,
        poll_interval=poll_interval
    )
    
    # Start monitoring
    monitor.run()


if __name__ == "__main__":
    main()

