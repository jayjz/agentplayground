"""Core enums"""
from enum import Enum


class SignalType(str, Enum):
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    EVENT_DRIVEN = "event_driven"
    RELATIVE_VALUE = "relative_value"
    MACRO = "macro"


class AgentStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"


class TradingMode(str, Enum):
    PAPER = "paper"
    LIVE = "live"
