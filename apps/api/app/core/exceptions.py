"""Custom exceptions"""


class AgentPlaygroundException(Exception):
    """Base exception"""
    pass


class DataProviderError(AgentPlaygroundException):
    """Data provider error"""
    pass


class AgentError(AgentPlaygroundException):
    """Agent execution error"""
    pass


class TradingError(AgentPlaygroundException):
    """Trading execution error"""
    pass


class ValidationError(AgentPlaygroundException):
    """Validation error"""
    pass
