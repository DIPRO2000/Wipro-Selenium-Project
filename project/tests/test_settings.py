"""Behavior checks for framework configuration."""

from __future__ import annotations

import unittest

from config.settings import load_settings


class SettingsTests(unittest.TestCase):
    def test_defaults_are_used_when_environment_is_empty(self) -> None:
        settings = load_settings({})

        self.assertEqual("https://automationexercise.com", settings.base_url)
        self.assertEqual(30.0, settings.request_timeout)
        self.assertEqual("INFO", settings.log_level)

    def test_environment_values_override_defaults(self) -> None:
        settings = load_settings(
            {
                "BASE_URL": "https://example.test",
                "REQUEST_TIMEOUT": "12.5",
                "LOG_LEVEL": "debug",
            }
        )

        self.assertEqual("https://example.test", settings.base_url)
        self.assertEqual(12.5, settings.request_timeout)
        self.assertEqual("DEBUG", settings.log_level)

    def test_zero_timeout_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "REQUEST_TIMEOUT must be a positive number"):
            load_settings({"REQUEST_TIMEOUT": "0"})

    def test_empty_base_url_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "BASE_URL must not be empty"):
            load_settings({"BASE_URL": "   "})

    def test_invalid_log_level_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "LOG_LEVEL must be a valid logging level"):
            load_settings({"LOG_LEVEL": "VERBOSE"})
