"""Behavior checks for logging and sensitive-data redaction."""

from __future__ import annotations

from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from framework.logging_utils import get_logger, log_sanitized, sanitize_data


class LoggingUtilsTests(unittest.TestCase):
    def test_sanitize_data_redacts_sensitive_values_recursively(self) -> None:
        payload = {
            "email": "test@example.com",
            "password": "secret123",
            "token": "abc123",
            "nested": [{"Authorization": "Bearer hidden"}],
        }

        sanitized = sanitize_data(payload)

        self.assertEqual("test@example.com", sanitized["email"])
        self.assertEqual("***REDACTED***", sanitized["password"])
        self.assertEqual("***REDACTED***", sanitized["token"])
        self.assertEqual("***REDACTED***", sanitized["nested"][0]["Authorization"])
        self.assertEqual("secret123", payload["password"])

    def test_logger_writes_sanitized_data_to_console_and_file(self) -> None:
        console = StringIO()
        with TemporaryDirectory() as temporary_directory:
            log_file = Path(temporary_directory) / "api_automation.log"
            logger = get_logger(
                "phase2.console_and_file",
                log_level="INFO",
                log_file=log_file,
                console_stream=console,
            )

            log_sanitized(
                logger,
                "INFO",
                "Login request",
                {"email": "test@example.com", "password": "secret123", "token": "abc123"},
            )
            for handler in logger.handlers:
                handler.flush()

            console_output = console.getvalue()
            file_output = log_file.read_text(encoding="utf-8")

        for output in (console_output, file_output):
            self.assertIn("Login request", output)
            self.assertIn("***REDACTED***", output)
            self.assertNotIn("secret123", output)
            self.assertNotIn("abc123", output)

    def test_logger_respects_configured_log_level(self) -> None:
        console = StringIO()
        with TemporaryDirectory() as temporary_directory:
            logger = get_logger(
                "phase2.log_level",
                log_level="ERROR",
                log_file=Path(temporary_directory) / "api_automation.log",
                console_stream=console,
            )

            logger.info("This message must be filtered")
            logger.error("This message must be logged")

        output = console.getvalue()
        self.assertNotIn("This message must be filtered", output)
        self.assertIn("This message must be logged", output)
