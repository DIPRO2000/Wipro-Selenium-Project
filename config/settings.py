"""Environment-based configuration for framework components."""

from __future__ import annotations

from dataclasses import dataclass
import math
import os
from collections.abc import Mapping


DEFAULT_BASE_URL = "https://automationexercise.com"
DEFAULT_REQUEST_TIMEOUT = 30.0
DEFAULT_LOG_LEVEL = "INFO"
VALID_LOG_LEVELS = frozenset(
    {"CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "NOTSET"}
)


@dataclass(frozen=True)
class Settings:
    """Validated settings consumed by future framework components."""

    base_url: str
    request_timeout: float
    log_level: str


def load_settings(environ: Mapping[str, str] | None = None) -> Settings:
    """Load validated settings from an environment-like mapping."""
    environment = os.environ if environ is None else environ
    return Settings(
        base_url=_read_base_url(environment.get("BASE_URL", DEFAULT_BASE_URL)),
        request_timeout=_read_timeout(
            environment.get("REQUEST_TIMEOUT", str(DEFAULT_REQUEST_TIMEOUT))
        ),
        log_level=_read_log_level(environment.get("LOG_LEVEL", DEFAULT_LOG_LEVEL)),
    )


def _read_base_url(value: str) -> str:
    base_url = value.strip()
    if not base_url:
        raise ValueError("BASE_URL must not be empty.")
    return base_url.rstrip("/")


def _read_timeout(value: str) -> float:
    try:
        timeout = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"REQUEST_TIMEOUT must be a positive number; got {value!r}."
        ) from error

    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError(f"REQUEST_TIMEOUT must be a positive number; got {value!r}.")
    return timeout


def _read_log_level(value: str) -> str:
    log_level = value.strip().upper()
    if log_level not in VALID_LOG_LEVELS:
        raise ValueError(
            f"LOG_LEVEL must be a valid logging level; got {value!r}. "
            f"Supported values: {', '.join(sorted(VALID_LOG_LEVELS))}."
        )
    return log_level
