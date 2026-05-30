"""Signal engine unit tests"""
import pytest
from app.services.signal_engine import SignalEngine
from datetime import datetime


def test_momentum_20d():
    """Test 20-day momentum calculation"""
    engine = SignalEngine()
    
    # Create price series with 10% gain over 20 days
    prices = [100] * 20 + [110]
    result = engine.calculate_momentum_20d(prices)
    
    assert result is not None
    assert abs(result - 0.10) < 0.001


def test_momentum_insufficient_data():
    """Test momentum with insufficient data"""
    engine = SignalEngine()
    prices = [100, 101, 102]
    
    result = engine.calculate_momentum_20d(prices)
    assert result is None


def test_volatility_20d():
    """Test volatility calculation"""
    engine = SignalEngine()
    # Create volatile price series
    prices = [100 + i * 0.5 + (i % 3) for i in range(25)]
    
    result = engine.calculate_volatility_20d(prices)
    assert result is not None
    assert result > 0


def test_generate_signals():
    """Test signal generation"""
    engine = SignalEngine()
    prices = [100 + i for i in range(70)]  # Steady uptrend
    signals = engine.generate_signals("test-asset", prices, datetime.now())
    
    assert len(signals) > 0
    signal_types = [s["signal_type"] for s in signals]
    assert "momentum_20d" in signal_types
    assert "momentum_60d" in signal_types
