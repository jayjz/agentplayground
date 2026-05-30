"""
Application configuration using Pydantic settings
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # Environment
    environment: str = "development"
    log_level: str = "INFO"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 30
    
    # Database
    database_url: str = "postgresql+asyncpg://agentplayground:agentplayground_dev_password@localhost:5432/agentplayground"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_cache_db: int = 1
    
    # DuckDB
    duckdb_path: str = "./data/analytics.duckdb"
    
    # LiteLLM
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    google_api_key: str | None = None
    groq_api_key: str | None = None
    litellm_model: str = "gpt-4o-mini"
    litellm_temperature: float = 0.1
    litellm_max_tokens: int = 4000
    
    # Prefect
    prefect_api_url: str = "http://localhost:4200/api"
    
    # Market Data
    alpha_vantage_api_key: str | None = None
    fred_api_key: str | None = None
    news_api_key: str | None = None
    sec_user_agent: str = "AgentPlayground/1.0"
    
    # Trading
    paper_trading_enabled: bool = True
    paper_trading_initial_balance: float = 1_000_000.0
    paper_trading_broker: str = "mock"
    live_trading_enabled: bool = False
    
    # OpenTelemetry
    otel_enabled: bool = False
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"
    otel_service_name: str = "agentplayground-api"


settings = Settings()
