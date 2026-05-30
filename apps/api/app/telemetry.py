"""OpenTelemetry instrumentation setup - disabled for P0"""
def setup_telemetry() -> None:
    """Initialize OpenTelemetry tracing - no-op for P0"""
    pass

def instrument_app(app) -> None:
    """Instrument FastAPI application - no-op for P0"""
    pass
