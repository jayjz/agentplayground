"""Paper broker for simulated order execution"""
from typing import Dict, Any
from datetime import datetime
import uuid


class PaperBroker:
    """Simulated paper trading broker"""
    
    def __init__(self, initial_balance: float = 1_000_000.0):
        self.initial_balance = initial_balance
        self.cash = initial_balance
        self.positions = {}  # asset_id -> quantity
        self.orders = []
    
    def place_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Place and immediately fill a paper order"""
        order_id = str(uuid.uuid4())
        
        # Simulate immediate fill at market price
        # In real implementation, would fetch current market price
        fill_price = order.get("limit_price") or 100.0  # Mock price
        
        filled_order = {
            "id": order_id,
            "asset_id": order["asset_id"],
            "side": order["side"],
            "quantity": order["quantity"],
            "order_type": order.get("order_type", "market"),
            "limit_price": order.get("limit_price"),
            "fill_price": fill_price,
            "status": "filled",
            "filled_at": datetime.utcnow().isoformat(),
            "execution_mode": "paper",
            "commission": 0.0,  # No commission in paper trading
        }
        
        # Update positions
        asset_id = order["asset_id"]
        qty = order["quantity"] if order["side"] == "buy" else -order["quantity"]
        
        if asset_id in self.positions:
            self.positions[asset_id] += qty
        else:
            self.positions[asset_id] = qty
        
        # Update cash (simplified - no commission, no slippage)
        cost = qty * fill_price
        self.cash -= cost
        
        self.orders.append(filled_order)
        
        return filled_order
    
    def get_positions(self) -> Dict[str, Any]:
        """Get current positions"""
        return {
            "cash": self.cash,
            "positions": self.positions,
            "total_value": self.cash + sum(qty * 100.0 for qty in self.positions.values()),
        }
