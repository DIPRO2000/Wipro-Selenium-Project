"""Reusable Requests client for future API automation steps."""

from __future__ import annotations

from collections.abc import Mapping
import logging
from typing import Any

import requests

from config.settings import Settings, load_settings
from framework.logging_utils import get_logger, log_sanitized


class ApiClient:
    """Send HTTP requests using shared configuration and sanitized logging."""

    def __init__(
        self,
        settings: Settings | None = None,
        session: requests.Session | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self.settings = settings or load_settings()
        self.session = session or requests.Session()
        self.logger = logger or get_logger(log_level=self.settings.log_level)
        self.last_request: dict[str, Any] | None = None

    def get(
        self,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> requests.Response:
        """Send a GET request."""
        return self._send_request("GET", endpoint, params=params, headers=headers)

    def post(
        self,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        headers: Mapping[str, str] | None = None,
    ) -> requests.Response:
        """Send a POST request."""
        return self._send_request(
            "POST", endpoint, params=params, data=data, json=json, headers=headers
        )

    def put(
        self,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        headers: Mapping[str, str] | None = None,
    ) -> requests.Response:
        """Send a PUT request."""
        return self._send_request(
            "PUT", endpoint, params=params, data=data, json=json, headers=headers
        )

    def delete(
        self,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        headers: Mapping[str, str] | None = None,
    ) -> requests.Response:
        """Send a DELETE request."""
        return self._send_request(
            "DELETE", endpoint, params=params, data=data, json=json, headers=headers
        )

    def close(self) -> None:
        """Release the reusable Requests session owned by this client."""
        self.session.close()

    def _send_request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Mapping[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        headers: Mapping[str, str] | None = None,
    ) -> requests.Response:
        url = self._build_url(endpoint)
        self.last_request = {
            "method": method,
            "url": url,
            "params": params,
            "data": data,
            "json": json,
            "headers": headers,
        }
        self._log_request(method, url, params, data, json, headers)
        return self.session.request(
            method,
            url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            timeout=self.settings.request_timeout,
        )

    def _build_url(self, endpoint: str) -> str:
        if not endpoint or not endpoint.strip():
            raise ValueError("API endpoint must not be empty.")
        return f"{self.settings.base_url}/{endpoint.lstrip('/')}"

    def _log_request(
        self,
        method: str,
        url: str,
        params: Mapping[str, Any] | None,
        data: Any,
        json: Any,
        headers: Mapping[str, str] | None,
    ) -> None:
        try:
            log_sanitized(
                self.logger,
                "INFO",
                "API request",
                {
                    "method": method,
                    "url": url,
                    "params": params,
                    "data": data,
                    "json": json,
                    "headers": headers,
                },
            )
        except Exception:
            self._log_failure_without_request_data()

    def _log_failure_without_request_data(self) -> None:
        try:
            self.logger.debug("Request logging failed.", exc_info=True)
        except Exception:
            pass
