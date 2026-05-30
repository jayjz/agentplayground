"""Seed endpoint for P0 - populates memory store with sample data"""
from fastapi import APIRouter
from app.services.signal_engine import SignalEngine
from app.services.audit_service import write_audit
from datetime import datetime, timedelta
import random

router = APIRouter()

# Set seed for deterministic data
random.seed(42)

@router.post("/seed")
async def seed_data():
    """Seed the database with sample data"""
    
    # Clear existing data
    
    # Sample assets
    assets = [
        {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Technology", "asset_type": "stock"},
        {"symbol": "MSFT", "name": "Microsoft", "sector": "Technology", "asset_type": "stock"},
        {"symbol": "GOOGL", "name": "Alphabet", "sector": "Technology", "asset_type": "stock"},
        {"symbol": "AMZN", "name": "Amazon", "sector": "Consumer Discretionary", "asset_type": "stock"},
        {"symbol": "TSLA", "name": "Tesla", "sector": "Consumer Discretionary", "asset_type": "stock"},
        {"symbol": "JPM", "name": "JPMorgan", "sector": "Financials", "asset_type": "stock"},
        {"symbol": "JNJ", "name": "Johnson & Johnson", "sector": "Healthcare", "asset_type": "stock"},
        {"symbol": "V", "name": "Visa", "sector": "Financials", "asset_type": "stock"},
        {"symbol": "PG", "name": "Procter & Gamble", "sector": "Consumer Staples", "asset_type": "stock"},
        {"symbol": "UNH", "name": "UnitedHealth", "sector": "Healthcare", "asset_type": "stock"},
    ]
    
    # Add assets
    for asset in assets:
        store.add_asset(asset)
    
    # Write audit log
    store.add_audit({
        "action": "seed_assets",
        "entity_type": "asset",
        "metadata": {"count": len(assets)}
    })
    
    # Generate signals using signal engine
    engine = SignalEngine()
    base_prices = [150, 300, 140, 130, 200, 140, 160, 220, 150, 500]
    
    for i, asset in enumerate(assets):
        # Generate deterministic price history
        prices = []
        price = base_prices[i]
        for _ in range(70):
            change = random.gauss(0, 0.02)
            price = price * (1 + change)
            prices.append(round(price, 2))
        
        # Generate signals
        signals = engine.generate_signals(
            asset_id=asset["symbol"],
            prices=prices,
            as_of_date=datetime.now()
        )
        
        for signal in signals:
            signal["ticker"] = asset["symbol"]
            store.add_signal(signal)
    
    # Write audit log
    store.add_audit({
        "action": "generate_signals",
        "entity_type": "signal",
        "metadata": {"count": len(store.get_signals())}
    })
    
    return {
        "status": "seeded",
        "assets": len(assets),
        "signals": len(store.get_signals()),
        "audits": len(store.get_audits()),
    }
