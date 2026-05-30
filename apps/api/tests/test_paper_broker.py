"""Paper broker tests"""
import pytest
from app.services.paper_broker import PaperBroker


def test_paper_broker_initialization():
    """Test broker initialization"""
    broker = PaperBroker(initial_balance=100000)
    assert broker.cash == 100000
    assert broker.initial_balance == 100000
    assert len(broker.positions) == 0


def test_place_buy_order():
    """Test placing a buy order"""
    broker = PaperBroker(initial_balance=100000)
    
    order = {
        "asset_id": "AAPL",
        "side": "buy",
        "quantity": 10,
        "order_type": "market",
    }
    
    result = broker.place_order(order)
    
    assert result["status"] == "filled"
    assert result["asset_id"] == "AAPL"
    assert result["quantity"] == 10
    assert result["side"] == "buy"
    assert "AAPL" in broker.positions
    assert broker.positions["AAPL"] == 10


def test_place_sell_order():
    """Test placing a sell order"""
    broker = PaperBroker(initial_balance=100000)
    
    # Buy first
    broker.place_order({
        "asset_id": "AAPL",
        "side": "buy",
        "quantity": 10,
        "order_type": "market",
    })
    
    # Then sell
    result = broker.place_order({
        "asset_id": "AAPL",
        "side": "sell",
        "quantity": 5,
        "order_type": "market",
    })
    
    assert result["status"] == "filled"
    assert broker.positions["AAPL"] == 5


def test_get_positions():
    """Test getting positions"""
    broker = PaperBroker(initial_balance=100000)
    
    broker.place_order({
        "asset_id": "AAPL",
        "side": "buy",
        "quantity": 10,
        "order_type": "market",
    })
    
    positions = broker.get_positions()
    
    assert "cash" in positions
    assert "positions" in positions
    assert "total_value" in positions
    assert positions["positions"]["AAPL"] == 10
