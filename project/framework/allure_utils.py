"""Small, sanitized Allure attachment helpers for API scenarios."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from typing import Any

import allure

from framework.logging_utils import REDACTED_VALUE, sanitize_data


_SENSITIVE_TEXT_PATTERN = re.compile(
    r"(?i)([\"']?(?:password|authorization|token|access_token|refresh_token)[\"']?\s*[:=]\s*)"
    r"([\"']?)([^,}\s\"']+)(\2)"
)


def attach_http_exchange(
    request: Mapping[str, Any],
    response: Any,
    *,
    name_prefix: str = "API",
) -> None:
    """Attach sanitized request metadata and response data without failing tests."""
    try:
        _attach_text(
            f"{name_prefix} request",
            _serialize(sanitize_data(dict(request))),
        )
        _attach_text(
            f"{name_prefix} response",
            _serialize(_response_data(response)),
        )
    except Exception:
        # Reporting must never mask the API result or a validation failure.
        return


def _response_data(response: Any) -> dict[str, Any]:
    try:
        body = sanitize_data(response.json())
    except (AttributeError, TypeError, ValueError):
        body = _sanitize_text(str(getattr(response, "text", "")))

    return {
        "status_code": getattr(response, "status_code", None),
        "headers": sanitize_data(dict(getattr(response, "headers", {}) or {})),
        "body": body,
    }


def _sanitize_text(value: str) -> str:
    return _SENSITIVE_TEXT_PATTERN.sub(
        rf"\g<1>{REDACTED_VALUE}",
        value,
    )


def _serialize(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, default=str)


def _attach_text(name: str, body: str) -> None:
    allure.attach(body, name=name, attachment_type=allure.attachment_type.TEXT)
