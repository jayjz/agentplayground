"""
OpenTelemetry instrumentation setup
"""
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource

from app.config import settings


def setup_telemetry() -> None:
    """Initialize OpenTelemetry tracing"""
    if not settings.otel_enabled:
        return
    
    resource = Resource.create({
        "service.name": settings.otel_service_name,
        "service.version": "0.1.0",
    })
    
    provider = TracerProvider(resource=resource)
    
    otlp_exporter = OTLPSpanExporter(
        endpoint=settings.otel_exporter_otlp_endpoint,
        insecure=True,
    )
    
    processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(processor)
    
    trace.set_tracer_provider(provider)


def instrument_app(app) -> None:
    """Instrument FastAPI application"""
    if settings.otel_enabled:
        FastAPIInstrumentor.instrument_app(app)
