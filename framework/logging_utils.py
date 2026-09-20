"""Logging setup and sensitive-data sanitization helpers."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
import logging
from typing import Any, TextIO


DEFAULT_LOG_FILE = Path("logs") / "api_automation.log"
REDACTED_VALUE = "***REDACTED***"
SENSITIVE_FIELD_NAMES = frozenset(
    {"password", "authorization", "token", "access_token", "refresh_token"}
)
_HANDLER_MARKER = "_api_automation_handler"
_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def sanitize_data(value: Any) -> Any:
    """Return a copy of nested request-like data with sensitive values redacted."""
    if isinstance(value, Mapping):
        return {
            key: REDACTED_VALUE if _is_sensitive_key(key) else sanitize_data(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [sanitize_data(item) for item in value]
    if isinstance(value, tuple):
        return tuple(sanitize_data(item) for item in value)
    return value


def get_logger(
    name: str = "api_automation",
    log_level: str | int = "INFO",
    log_file: Path | str = DEFAULT_LOG_FILE,
    console_stream: TextIO | None = None,
) -> logging.Logger:
    """Create a logger with one console handler and one file handler."""
    logger = logging.getLogger(name)
    logger.setLevel(_resolve_log_level(log_level))
    logger.propagate = False
    _remove_configured_handlers(logger)

    formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)
    console_handler = logging.StreamHandler(console_stream)
    console_handler.setFormatter(formatter)
    _mark_handler(console_handler)

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    _mark_handler(file_handler)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


def log_sanitized(
    logger: logging.Logger,
    level: str | int,
    message: str,
    data: Any,
) -> None:
    """Log a message with a sanitized representation of request-like data."""
    logger.log(_resolve_log_level(level), "%s | data=%s", message, sanitize_data(data))


def _is_sensitive_key(key: Any) -> bool:
    if not isinstance(key, str):
        return False
    normalized_key = key.strip().lower().replace("-", "_")
    return normalized_key in SENSITIVE_FIELD_NAMES


def _resolve_log_level(level: str | int) -> int:
    if isinstance(level, int):
        return level
    if isinstance(level, str):
        resolved_level = logging.getLevelName(level.strip().upper())
        if isinstance(resolved_level, int):
            return resolved_level
    raise ValueError(f"Invalid log level: {level!r}.")


def _mark_handler(handler: logging.Handler) -> None:
    setattr(handler, _HANDLER_MARKER, True)


def _remove_configured_handlers(logger: logging.Logger) -> None:
    for handler in logger.handlers[:]:
        if getattr(handler, _HANDLER_MARKER, False):
            logger.removeHandler(handler)
            handler.close()
