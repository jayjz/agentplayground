#!/usr/bin/env python3
"""Seed script with deterministic sample data"""
import json
import random
from datetime import datetime, timedelta

# Deterministic seed for reproducible data
random.seed(42)

# Sample assets
ASSETS = [
    {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Technology", "industry": "Consumer Electronics"},
    {"symbol": "MSFT", "name": "Microsoft Corporation", "sector": "Technology", "industry": "Software"},
    {"symbol": "GOOGL", "name": "Alphabet Inc.", "sector": "Technology", "industry": "Internet"},
    {"symbol": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumer Discretionary", "industry": "E-Commerce"},
    {"symbol": "TSLA", "name": "Tesla Inc.", "sector": "Consumer Discretionary", "industry": "Auto Manufacturers"},
    {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "sector": "Financials", "industry": "Banks"},
    {"symbol": "JNJ", "name": "Johnson & Johnson", "sector": "Healthcare", "industry": "Drug Manufacturers"},
    {"symbol": "V", "name": "Visa Inc.", "sector": "Financials", "industry": "Credit Services"},
    {"symbol": "PG", "name": "Procter & Gamble Co.", "sector": "Consumer Staples", "industry": "Household Products"},
    {"symbol": "UNH", "name": "UnitedHealth Group Inc.", "sector": "Healthcare", "industry": "Healthcare Plans"},
]

def generate_price_history(base_price: float, days: int = 252) -> list:
    """Generate deterministic price history"""
    prices = []
    price = base_price
    
    for i in range(days):
        # Deterministic random walk
        change = random.gauss(0, 0.02)  # 2% daily vol
        price = price * (1 + change)
        prices.append(round(price, 2))
    
    return prices

def main():
    """Generate and print sample data"""
    print("Generating deterministic sample data...")
    print(f"Assets: {len(ASSETS)}")
    
    sample_data = {
        "assets": ASSETS,
        "generated_at": datetime.now().isoformat(),
        "price_histories": {}
    }
    
    # Generate price histories
    base_prices = [150, 300, 140, 130, 200, 140, 160, 220, 150, 500]
    for i, asset in enumerate(ASSETS):
        prices = generate_price_history(base_prices[i])
        sample_data["price_histories"][asset["symbol"]] = prices[-60:]  # Last 60 days
    
    # Save to file
    with open("data/sample/seed_data.json", "w") as f:
        json.dump(sample_data, f, indent=2)
    
    print("✓ Sample data saved to data/sample/seed_data.json")
    print(f"✓ Generated {sum(len(v) for v in sample_data['price_histories'].values())} price points")

if __name__ == "__main__":
    import os
    os.makedirs("data/sample", exist_ok=True)
    main()
