from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


def _env(key: str, default: str | None = None) -> str | None:
    v = os.getenv(key)
    if v is None or v == "":
        return default
    return v


def _env_bool(key: str, default: bool = False) -> bool:
    raw = _env(key)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    database_url: str = _env("DATABASE_URL", "sqlite:///./secura.db")  # local dev default
    cors_allow_origins: str = _env("CORS_ALLOW_ORIGINS", "*") or "*"

    jwt_secret: str = _env("JWT_SECRET", "dev-insecure-change-me") or "dev-insecure-change-me"
    jwt_issuer: str = _env("JWT_ISSUER", "secura-ai") or "secura-ai"
    jwt_exp_minutes: int = int(_env("JWT_EXP_MINUTES", "480") or "480")

    rate_limit: int = int(_env("RATE_LIMIT", "10") or "10")
    rate_window_seconds: int = int(_env("RATE_WINDOW", "60") or "60")

    redis_url: str = _env("REDIS_URL", "redis://localhost:6379/0") or "redis://localhost:6379/0"
    rq_queue: str = _env("RQ_QUEUE", "secura") or "secura"

    auto_create_schema: bool = _env_bool("AUTO_CREATE_SCHEMA", False)
    bootstrap_token: str | None = _env("BOOTSTRAP_TOKEN", None)


settings = Settings()

