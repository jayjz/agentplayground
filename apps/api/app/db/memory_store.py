"""In-memory data store for P0 vertical slice"""
from typing import Dict, List, Any
import json
import os
from datetime import datetime

class MemoryStore:
    """Simple in-memory store with file backup"""
    
    def __init__(self, data_file: str = "data/memory_store.json"):
        self.data_file = data_file
        self.data = {
            "assets": [],
            "signals": [],
            "events": [],
            "trade_candidates": [],
            "order_proposals": [],
            "audits": [],
        }
        self.load()
    
    def load(self):
        """Load data from file if exists"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
            except:
                pass
    
    def save(self):
        """Save data to file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
    
    def add_asset(self, asset: Dict[str, Any]):
        asset["id"] = asset.get("id", f"asset_{len(self.data['assets']) + 1}")
        asset["created_at"] = datetime.now().isoformat()
        self.data["assets"].append(asset)
        self.save()
        return asset
    
    def get_assets(self) -> List[Dict[str, Any]]:
        return self.data["assets"]
    
    def add_signal(self, signal: Dict[str, Any]):
        signal["id"] = signal.get("id", f"signal_{len(self.data['signals']) + 1}")
        signal["created_at"] = datetime.now().isoformat()
        self.data["signals"].append(signal)
        self.save()
        return signal
    
    def get_signals(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self.data["signals"][-limit:]
    
    def add_audit(self, audit: Dict[str, Any]):
        audit["id"] = audit.get("id", f"audit_{len(self.data['audits']) + 1}")
        audit["created_at"] = datetime.now().isoformat()
        self.data["audits"].append(audit)
        self.save()
        return audit
    
    def get_audits(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self.data["audits"][-limit:]

# Global store instance
store = MemoryStore()
