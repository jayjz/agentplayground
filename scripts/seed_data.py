#!/usr/bin/env python3
"""Seed script - populate local SQLite database with deterministic sample data."""

from __future__ import annotations

import asyncio
import os
import random
import sys
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from sqlalchemy import delete, select

# Ensure the API package is importable when running from the repo root/scripts directory.
REPO_ROOT = Path(__file__).resolve().parent.parent
API_ROOT = REPO_ROOT / "apps" / "api"
if str(API_ROOT) not in sys.path:
    sys.path.insert(0, str(API_ROOT))

from app.db.base import Base  # noqa: E402
from app.db.models.asset import Asset  # noqa: E402
from app.db.models.audit_log import AuditLog  # noqa: E402
from app.db.models.factor_signal import FactorSignal  # noqa: E402
from app.db.session import AsyncSessionLocal, engine  # noqa: E402
from app.services.signal_engine import SignalEngine  # noqa: E402

SEED_RANDOM = random.Random(42)

ASSET_UNIVERSE: list[dict[str, Any]] = [
    # Large-cap tech / AI / semis
    {"symbol": "AAPL", "name": "Apple Inc.", "asset_type": "stock", "sector": "Technology", "industry": "Consumer Electronics", "exchange": "NASDAQ"},
    {"symbol": "MSFT", "name": "Microsoft Corporation", "asset_type": "stock", "sector": "Technology", "industry": "Software", "exchange": "NASDAQ"},
    {"symbol": "GOOGL", "name": "Alphabet Inc.", "asset_type": "stock", "sector": "Technology", "industry": "Internet Content & Information", "exchange": "NASDAQ"},
    {"symbol": "AMZN", "name": "Amazon.com Inc.", "asset_type": "stock", "sector": "Consumer Discretionary", "industry": "Internet Retail", "exchange": "NASDAQ"},
    {"symbol": "META", "name": "Meta Platforms Inc.", "asset_type": "stock", "sector": "Technology", "industry": "Internet Content & Information", "exchange": "NASDAQ"},
    {"symbol": "NVDA", "name": "NVIDIA Corporation", "asset_type": "stock", "sector": "Technology", "industry": "Semiconductors", "exchange": "NASDAQ"},
    {"symbol": "AMD", "name": "Advanced Micro Devices Inc.", "asset_type": "stock", "sector": "Technology", "industry": "Semiconductors", "exchange": "NASDAQ"},
    {"symbol": "AVGO", "name": "Broadcom Inc.", "asset_type": "stock", "sector": "Technology", "industry": "Semiconductors", "exchange": "NASDAQ"},

    # Consumer / discretionary
    {"symbol": "TSLA", "name": "Tesla Inc.", "asset_type": "stock", "sector": "Consumer Discretionary", "industry": "Auto Manufacturers", "exchange": "NASDAQ"},
    {"symbol": "NFLX", "name": "Netflix Inc.", "asset_type": "stock", "sector": "Communication Services", "industry": "Entertainment", "exchange": "NASDAQ"},
    {"symbol": "MCD", "name": "McDonald's Corporation", "asset_type": "stock", "sector": "Consumer Discretionary", "industry": "Restaurants", "exchange": "NYSE"},
    {"symbol": "SBUX", "name": "Starbucks Corporation", "asset_type": "stock", "sector": "Consumer Discretionary", "industry": "Restaurants", "exchange": "NASDAQ"},
    {"symbol": "NKE", "name": "NIKE Inc.", "asset_type": "stock", "sector": "Consumer Discretionary", "industry": "Footwear & Accessories", "exchange": "NYSE"},

    # Financials
    {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "asset_type": "stock", "sector": "Financials", "industry": "Banks - Diversified", "exchange": "NYSE"},
    {"symbol": "GS", "name": "Goldman Sachs Group Inc.", "asset_type": "stock", "sector": "Financials", "industry": "Capital Markets", "exchange": "NYSE"},
    {"symbol": "MS", "name": "Morgan Stanley", "asset_type": "stock", "sector": "Financials", "industry": "Capital Markets", "exchange": "NYSE"},
    {"symbol": "V", "name": "Visa Inc.", "asset_type": "stock", "sector": "Financials", "industry": "Credit Services", "exchange": "NYSE"},
    {"symbol": "MA", "name": "Mastercard Incorporated", "asset_type": "stock", "sector": "Financials", "industry": "Credit Services", "exchange": "NYSE"},

    # Healthcare
    {"symbol": "JNJ", "name": "Johnson & Johnson", "asset_type": "stock", "sector": "Healthcare", "industry": "Drug Manufacturers - General", "exchange": "NYSE"},
    {"symbol": "UNH", "name": "UnitedHealth Group Incorporated", "asset_type": "stock", "sector": "Healthcare", "industry": "Healthcare Plans", "exchange": "NYSE"},
    {"symbol": "LLY", "name": "Eli Lilly and Company", "asset_type": "stock", "sector": "Healthcare", "industry": "Drug Manufacturers - General", "exchange": "NYSE"},
    {"symbol": "PFE", "name": "Pfizer Inc.", "asset_type": "stock", "sector": "Healthcare", "industry": "Drug Manufacturers - General", "exchange": "NYSE"},

    # Industrials / cyclicals
    {"symbol": "CAT", "name": "Caterpillar Inc.", "asset_type": "stock", "sector": "Industrials", "industry": "Farm & Heavy Construction Machinery", "exchange": "NYSE"},
    {"symbol": "GE", "name": "GE Aerospace", "asset_type": "stock", "sector": "Industrials", "industry": "Aerospace & Defense", "exchange": "NYSE"},
    {"symbol": "HON", "name": "Honeywell International Inc.", "asset_type": "stock", "sector": "Industrials", "industry": "Conglomerates", "exchange": "NASDAQ"},
    {"symbol": "DE", "name": "Deere & Company", "asset_type": "stock", "sector": "Industrials", "industry": "Farm & Heavy Construction Machinery", "exchange": "NYSE"},

    # Energy
    {"symbol": "XOM", "name": "Exxon Mobil Corporation", "asset_type": "stock", "sector": "Energy", "industry": "Oil & Gas Integrated", "exchange": "NYSE"},
    {"symbol": "CVX", "name": "Chevron Corporation", "asset_type": "stock", "sector": "Energy", "industry": "Oil & Gas Integrated", "exchange": "NYSE"},
    {"symbol": "SLB", "name": "Schlumberger Limited", "asset_type": "stock", "sector": "Energy", "industry": "Oil & Gas Equipment & Services", "exchange": "NYSE"},

    # ETFs / macro proxies
    {"symbol": "SPY", "name": "SPDR S&P 500 ETF Trust", "asset_type": "etf", "sector": "Index", "industry": "Large Blend", "exchange": "NYSEARCA"},
    {"symbol": "QQQ", "name": "Invesco QQQ Trust", "asset_type": "etf", "sector": "Index", "industry": "Large Growth", "exchange": "NASDAQ"},
    {"symbol": "IWM", "name": "iShares Russell 2000 ETF", "asset_type": "etf", "sector": "Index", "industry": "Small Blend", "exchange": "NYSEARCA"},
    {"symbol": "XLF", "name": "Financial Select Sector SPDR Fund", "asset_type": "etf", "sector": "Financials", "industry": "Sector ETF", "exchange": "NYSEARCA"},
    {"symbol": "XLV", "name": "Health Care Select Sector SPDR Fund", "asset_type": "etf", "sector": "Healthcare", "industry": "Sector ETF", "exchange": "NYSEARCA"},
    {"symbol": "XLE", "name": "Energy Select Sector SPDR Fund", "asset_type": "etf", "sector": "Energy", "industry": "Sector ETF", "exchange": "NYSEARCA"},
    {"symbol": "TLT", "name": "iShares 20+ Year Treasury Bond ETF", "asset_type": "etf", "sector": "Rates", "industry": "Treasury ETF", "exchange": "NASDAQ"},
    {"symbol": "GLD", "name": "SPDR Gold Shares", "asset_type": "etf", "sector": "Commodities", "industry": "Gold ETF", "exchange": "NYSEARCA"},
    {"symbol": "USO", "name": "United States Oil Fund LP", "asset_type": "etf", "sector": "Commodities", "industry": "Oil ETF", "exchange": "NYSEARCA"},
]


def generate_price_series(
    start_price: float,
    length: int = 90,
    drift: float = 0.0005,
    volatility: float = 0.02,
) -> list[float]:
    """Generate a deterministic synthetic price series."""
    prices: list[float] = []
    price = start_price

    for _ in range(length):
        shock = SEED_RANDOM.gauss(drift, volatility)
        price = max(5.0, price * (1 + shock))
        prices.append(round(price, 2))

    return prices


def build_start_price(asset_type: str, index: int) -> float:
    """Create deterministic but varied starting prices."""
    if asset_type == "etf":
        return 80.0 + (index * 7.5)
    return 40.0 + (index * 13.0)


async def init_tables() -> None:
    """Create all tables for local development if they do not exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def clear_seed_tables() -> None:
    """Clear seeded tables in dependency-safe order for idempotent reseeding."""
    async with AsyncSessionLocal() as db:
        await db.execute(delete(FactorSignal))
        await db.execute(delete(AuditLog))
        await db.execute(delete(Asset))
        await db.commit()


async def seed_assets_and_signals() -> tuple[int, int]:
    """Insert assets and generated factor signals."""
    signal_engine = SignalEngine()
    asset_count = 0
    signal_count = 0

    async with AsyncSessionLocal() as db:
        assets: list[Asset] = []

        for index, asset_data in enumerate(ASSET_UNIVERSE):
            asset = Asset(
                **asset_data,
                is_active=True,
            )
            db.add(asset)
            assets.append(asset)

        await db.flush()

        asset_count = len(assets)

        for index, asset in enumerate(assets):
            prices = generate_price_series(
                start_price=build_start_price(asset.asset_type, index),
                length=90,
                drift=0.0007 if asset.asset_type == "stock" else 0.0003,
                volatility=0.022 if asset.asset_type == "stock" else 0.012,
            )

            generated = signal_engine.generate_signals(
                asset_id=str(asset.id),
                prices=prices,
                as_of_date=datetime.utcnow(),
            )

            for signal_data in generated:
                signal = FactorSignal(
                    asset_id=asset.id,
                    signal_date=datetime.utcnow().date(),
                    signal_type=signal_data["signal_type"],
                    raw_value=Decimal(str(signal_data["raw_value"])) if signal_data.get("raw_value") is not None else None,
                    normalized_value=Decimal(str(signal_data["normalized_value"])) if signal_data.get("normalized_value") is not None else None,
                    score=Decimal(str(signal_data["score"])) if signal_data.get("score") is not None else None,
                    confidence=Decimal(str(signal_data["confidence"])) if signal_data.get("confidence") is not None else None,
                    horizon=signal_data.get("horizon"),
                    rationale=signal_data.get("rationale"),
                )
                db.add(signal)
                signal_count += 1

        await db.commit()

    return asset_count, signal_count


async def seed_audits(asset_count: int, signal_count: int) -> int:
    """Insert audit logs describing the seed operation."""
    audit_rows = [
        AuditLog(
            actor_type="system",
            action="seed_started",
            entity_type="database",
            extra_data={"timestamp": datetime.utcnow().isoformat()},
        ),
        AuditLog(
            actor_type="system",
            action="assets_seeded",
            entity_type="asset",
            extra_data={"count": asset_count},
        ),
        AuditLog(
            actor_type="system",
            action="signals_generated",
            entity_type="factor_signal",
            extra_data={"count": signal_count},
        ),
        AuditLog(
            actor_type="system",
            action="seed_completed",
            entity_type="database",
            extra_data={
                "assets": asset_count,
                "signals": signal_count,
                "timestamp": datetime.utcnow().isoformat(),
            },
        ),
    ]

    async with AsyncSessionLocal() as db:
        for row in audit_rows:
            db.add(row)
        await db.commit()

    return len(audit_rows)


async def seed_database() -> None:
    """Initialize tables and seed the local SQLite database."""
    print("Initializing local database...")
    await init_tables()

    print("Clearing existing seed data...")
    await clear_seed_tables()

    print("Seeding assets and signals...")
    asset_count, signal_count = await seed_assets_and_signals()

    print("Seeding audit logs...")
    audit_count = await seed_audits(asset_count, signal_count)

    print("Seed completed successfully.")
    print(f"Assets inserted: {asset_count}")
    print(f"Factor signals inserted: {signal_count}")
    print(f"Audit logs inserted: {audit_count}")


if __name__ == "__main__":
    asyncio.run(seed_database())
