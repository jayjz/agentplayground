#!/usr/bin/env python3
"""Seed script - writes to SQLite database"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'apps', 'api'))

from datetime import datetime, timedelta
import random
from app.db.session import AsyncSessionLocal
from app.db.models.asset import Asset
from app.db.models.factor_signal import FactorSignal
from app.db.models.audit_log import AuditLog
from app.services.signal_engine import SignalEngine

# Deterministic seed
random.seed(42)

ASSETS = [
    {"symbol": "AAPL", "name": "Apple Inc.", "asset_type": "stock", "sector": "Technology", "industry": "Consumer Electronics", "exchange": "NASDAQ"},
    {"symbol": "MSFT", "name": "Microsoft Corporation", "asset_type": "stock", "sector": "Technology", "industry": "Software", "exchange": "NASDAQ"},
    {"symbol": "GOOGL", "name": "Alphabet Inc.", "asset_type": "stock", "sector": "Technology", "industry": "Internet", "exchange": "NASDAQ"},
    {"symbol": "AMZN", "name": "Amazon.com Inc.", "asset_type": "stock", "sector": "Consumer Discretionary", "industry": "E-Commerce", "exchange": "NASDAQ"},
    {"symbol": "TSLA", "name": "Tesla Inc.", "asset_type": "stock", "sector": "Consumer Discretionary", "industry": "Auto Manufacturers", "exchange": "NASDAQ"},
    {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "asset_type": "stock", "sector": "Financials", "industry": "Banks", "exchange": "NYSE"},
    {"symbol": "JNJ", "name": "Johnson & Johnson", "asset_type": "stock", "sector": "Healthcare", "industry": "Drug Manufacturers", "exchange": "NYSE"},
    {"symbol": "V", "name": "Visa Inc.", "asset_type": "stock", "sector": "Financials", "industry": "Credit Services", "exchange": "NYSE"},
    {"symbol": "PG", "name": "Procter & Gamble Co.", "asset_type": "stock", "sector": "Consumer Staples", "industry": "Household Products", "exchange": "NYSE"},
    {"symbol": "UNH", "name": "UnitedHealth Group Inc.", "asset_type": "stock", "sector": "Healthcare", "industry": "Healthcare Plans", "exchange": "NYSE"},
]

async def seed_database():
    """Seed the database with sample data"""
    async with AsyncSessionLocal() as db:
        print("Seeding database...")
        
        # Create audit log for seed start
        audit_start = AuditLog(
            actor_type="system",
            action="seed_started",
            entity_type="database",
            extra_data={"timestamp": datetime.now().isoformat()}
        )
        db.add(audit_start)
        
        # Add assets
        assets = []
        for asset_data in ASSETS:
            asset = Asset(**asset_data)
            db.add(asset)
            assets.append(asset)
        
        await db.flush()
        print(f"✓ Created {len(assets)} assets")
        
        # Create audit log
        audit_assets = AuditLog(
            actor_type="system",
            action="assets_seeded",
            entity_type="asset",
            extra_data={"count": len(assets)}
        )
        db.add(audit_assets)
        
        # Generate signals
        engine = SignalEngine()
        base_prices = [150, 300, 140, 130, 200, 140, 160, 220, 150, 500]
        signal_count = 0
        
        for i, asset in enumerate(assets):
            # Generate price history
            prices = []
            price = base_prices[i]
            for _ in range(70):
                change = random.gauss(0, 0.02)
                price = price * (1 + change)
                prices.append(round(price, 2))
            
            # Generate signals
            signals_data = engine.generate_signals(
                asset_id=str(asset.id),
                prices=prices,
                as_of_date=datetime.now()
            )
            
            for sig_data in signals_data:
                signal = FactorSignal(
                    asset_id=asset.id,
                    signal_date=datetime.now().date(),
                    signal_type=sig_data["signal_type"],
                    raw_value=sig_data.get("raw_value"),
                    normalized_value=sig_data.get("normalized_value"),
                    score=sig_data["score"],
                    confidence=sig_data["confidence"],
                    horizon=sig_data.get("horizon"),
                    rationale=sig_data.get("rationale")
                )
                db.add(signal)
                signal_count += 1
        
        await db.flush()
        print(f"✓ Created {signal_count} signals")
        
        # Create audit log for signals
        audit_signals = AuditLog(
            actor_type="system",
            action="signals_generated",
            entity_type="factor_signal",
            extra_data={"count": signal_count}
        )
        db.add(audit_signals)
        
        # Final audit log
        audit_complete = AuditLog(
            actor_type="system",
            action="seed_completed",
            entity_type="database",
            extra_data={
                "assets": len(assets),
                "signals": signal_count,
                "timestamp": datetime.now().isoformat()
            }
        )
        db.add(audit_complete)
        
        await db.commit()
        print("✓ Database seeded successfully")
        print(f"✓ Total: {len(assets)} assets, {signal_count} signals, 4 audit logs")

if __name__ == "__main__":
    asyncio.run(seed_database())
