"""Behavior checks for the reusable API client."""

from __future__ import annotations

from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock

import requests

from config.settings import Settings
from framework.api_client import ApiClient
from framework.logging_utils import get_logger


class ApiClientTests(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = Settings(
            base_url="https://service.example",
            request_timeout=12.5,
            log_level="INFO",
        )
        self.session = Mock(spec=requests.Session)
        self.response = Mock(spec=requests.Response)
        self.session.request.return_value = self.response
        self.logger = Mock()
        self.client = ApiClient(
            settings=self.settings,
            session=self.session,
            logger=self.logger,
        )

    def test_get_builds_url_uses_timeout_and_returns_original_response(self) -> None:
        response = self.client.get("/api/productsList", params={"page": "1"})

        self.assertIs(self.response, response)
        self.session.request.assert_called_once_with(
            "GET",
            "https://service.example/api/productsList",
            params={"page": "1"},
            data=None,
            json=None,
            headers=None,
            timeout=12.5,
        )

    def test_post_sends_form_data_through_shared_request_boundary(self) -> None:
        self.client.post("api/login", data={"email": "test@example.com"})

        self.session.request.assert_called_once_with(
            "POST",
            "https://service.example/api/login",
            params=None,
            data={"email": "test@example.com"},
            json=None,
            headers=None,
            timeout=12.5,
        )

    def test_last_request_metadata_is_available_for_reporting(self) -> None:
        self.client.post(
            "/api/login",
            params={"source": "test"},
            data={"password": "secret123"},
            headers={"Authorization": "Bearer hidden"},
        )

        self.assertEqual(
            self.client.last_request,
            {
                "method": "POST",
                "url": "https://service.example/api/login",
                "params": {"source": "test"},
                "data": {"password": "secret123"},
                "json": None,
                "headers": {"Authorization": "Bearer hidden"},
            },
        )

    def test_put_sends_json_body_through_shared_request_boundary(self) -> None:
        self.client.put("/api/account", json={"name": "Updated User"})

        self.session.request.assert_called_once_with(
            "PUT",
            "https://service.example/api/account",
            params=None,
            data=None,
            json={"name": "Updated User"},
            headers=None,
            timeout=12.5,
        )

    def test_delete_sends_query_parameters_through_shared_request_boundary(self) -> None:
        self.client.delete("/api/account", params={"account_id": "42"})

        self.session.request.assert_called_once_with(
            "DELETE",
            "https://service.example/api/account",
            params={"account_id": "42"},
            data=None,
            json=None,
            headers=None,
            timeout=12.5,
        )

    def test_empty_endpoint_is_rejected_without_sending_a_request(self) -> None:
        with self.assertRaisesRegex(ValueError, "endpoint must not be empty"):
            self.client.get("   ")

        self.session.request.assert_not_called()

    def test_request_log_redacts_sensitive_form_json_and_header_values(self) -> None:
        console = StringIO()
        with TemporaryDirectory() as temporary_directory:
            logger = get_logger(
                "phase3.sanitized_request",
                log_level="INFO",
                log_file=Path(temporary_directory) / "api_automation.log",
                console_stream=console,
            )
            client = ApiClient(
                settings=self.settings,
                session=self.session,
                logger=logger,
            )

            client.post(
                "/api/login",
                data={"password": "secret123"},
                json={"token": "abc123"},
                headers={"Authorization": "Bearer hidden"},
            )

        output = console.getvalue()
        self.assertIn("API request", output)
        self.assertIn("***REDACTED***", output)
        self.assertNotIn("secret123", output)
        self.assertNotIn("abc123", output)
        self.assertNotIn("Bearer hidden", output)
