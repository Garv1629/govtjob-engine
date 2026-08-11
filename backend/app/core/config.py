from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application & Environment
    APP_NAME: str = "GovtJob AI Agent SaaS"
    APP_ENV: str = "production"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "production_super_secret_master_key_32bytes_min"

    # Network & Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: List[str] = ["*"]

    # Database & Redis
    DATABASE_URL: str = "postgresql+asyncpg://govtjob:production_secure_pass@postgres:5432/govtjob_db"
    REDIS_URL: str = "redis://redis:6379/0"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 3600

    # Encryption & JWT Auth
    ENCRYPTION_KEY: str = "32_byte_secret_encryption_key_hash_prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # AI Model Engine
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3-pro"

    # Telegram Bot Command Center
    TELEGRAM_BOT_TOKEN: str = "8934752999:AAFjyAQffdzCaWN5mEXnUy_K7Roe2QH338s"
    TELEGRAM_CHAT_ID: str = "2128933074"
    TELEGRAM_ALLOWED_USER_IDS: List[str] = ["2128933074", "*"]
    TELEGRAM_ENABLED: bool = True

    # Playwright Automation
    PLAYWRIGHT_HEADLESS: bool = True
    PLAYWRIGHT_SLOW_MO: int = 100
    PLAYWRIGHT_TIMEOUT_MS: int = 30000

    # Rate Limiting & Security
    RATE_LIMIT_PER_MINUTE: int = 120
    SECURITY_HEADERS_ENABLED: bool = True

    # Telemetry & Monitoring
    PROMETHEUS_METRICS_ENABLED: bool = True
    OPENTELEMETRY_SERVICE_NAME: str = "govtjob-orchestrator"

    # Workflow Orchestration Engine Configurations
    WORKFLOW_STEP_TIMEOUT_SECONDS: int = 120
    WORKFLOW_MAX_RETRIES: int = 3
    WORKFLOW_RETRY_BACKOFF_FACTOR: float = 2.0
    WORKFLOW_SCHEDULER_INTERVAL_SECONDS: int = 30
    WORKFLOW_AUTO_RECOVERY_ENABLED: bool = True
    WORKFLOW_METRICS_RETENTION_COUNT: int = 1000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["*"]


settings = Settings()
