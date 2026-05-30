"""Initialize database tables"""
import asyncio
import sys
sys.path.insert(0, '.')

from app.db.base import Base
from app.db.session import engine
from app.db.models import *  # Import all models

async def init_db():
    """Create all tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Database tables created")

if __name__ == "__main__":
    asyncio.run(init_db())
