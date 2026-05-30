"""Signal engine with deterministic factor calculations"""
from typing import List, Dict, Any
import statistics
from datetime import datetime, timedelta


class SignalEngine:
    """Deterministic signal generation engine"""
    
    def __init__(self):
        self.min_history_days = 60
    
    def calculate_momentum_20d(self, prices: List[float]) -> float | None:
        """Calculate 20-day momentum"""
        if len(prices) < 21:
            return None
        return prices[-1] / prices[-21] - 1.0
    
    def calculate_momentum_60d(self, prices: List[float]) -> float | None:
        """Calculate 60-day momentum"""
        if len(prices) < 61:
            return None
        return prices[-1] / prices[-61] - 1.0
    
    def calculate_volatility_20d(self, prices: List[float]) -> float | None:
        """Calculate 20-day volatility"""
        if len(prices) < 21:
            return None
        returns = [(prices[i] / prices[i-1] - 1) for i in range(1, min(21, len(prices)))]
        if len(returns) < 2:
            return None
        return statistics.stdev(returns) if len(returns) > 1 else 0.0
    
    def calculate_mean_reversion_5d(self, prices: List[float]) -> float | None:
        """Calculate 5-day mean reversion signal"""
        if len(prices) < 6:
            return None
        return -(prices[-1] / prices[-6] - 1.0)
    
    def generate_signals(self, asset_id: str, prices: List[float], 
                        as_of_date: datetime) -> List[Dict[str, Any]]:
        """Generate all signals for an asset"""
        signals = []
        
        # Momentum 20d
        mom_20 = self.calculate_momentum_20d(prices)
        if mom_20 is not None:
            signals.append({
                "asset_id": asset_id,
                "signal_type": "momentum_20d",
                "signal_date": as_of_date.date(),
                "raw_value": mom_20,
                "normalized_value": max(-1.0, min(1.0, mom_20 * 10)),
                "score": abs(mom_20),
                "confidence": 0.7,
                "horizon": "20d",
                "rationale": f"20-day momentum: {mom_20:.2%}",
            })
        
        # Momentum 60d
        mom_60 = self.calculate_momentum_60d(prices)
        if mom_60 is not None:
            signals.append({
                "asset_id": asset_id,
                "signal_type": "momentum_60d",
                "signal_date": as_of_date.date(),
                "raw_value": mom_60,
                "normalized_value": max(-1.0, min(1.0, mom_60 * 5)),
                "score": abs(mom_60),
                "confidence": 0.75,
                "horizon": "60d",
                "rationale": f"60-day momentum: {mom_60:.2%}",
            })
        
        # Volatility 20d
        vol_20 = self.calculate_volatility_20d(prices)
        if vol_20 is not None:
            signals.append({
                "asset_id": asset_id,
                "signal_type": "volatility_20d",
                "signal_date": as_of_date.date(),
                "raw_value": vol_20,
                "normalized_value": vol_20,
                "score": vol_20,
                "confidence": 0.8,
                "horizon": "20d",
                "rationale": f"20-day volatility: {vol_20:.2%}",
            })
        
        # Mean reversion 5d
        mr_5 = self.calculate_mean_reversion_5d(prices)
        if mr_5 is not None:
            signals.append({
                "asset_id": asset_id,
                "signal_type": "mean_reversion_5d",
                "signal_date": as_of_date.date(),
                "raw_value": mr_5,
                "normalized_value": max(-1.0, min(1.0, mr_5 * 10)),
                "score": abs(mr_5),
                "confidence": 0.6,
                "horizon": "5d",
                "rationale": f"5-day mean reversion: {mr_5:.2%}",
            })
        
        return signals
