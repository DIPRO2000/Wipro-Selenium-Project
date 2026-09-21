"""Behavior checks for disposable account data generation."""

from __future__ import annotations

import unittest

from framework.account_data import ACCOUNT_FIELD_NAMES, create_test_account


class AccountDataTests(unittest.TestCase):
    def test_generated_account_emails_are_unique(self) -> None:
        first_account = create_test_account()
        second_account = create_test_account()

        self.assertNotEqual(first_account.email, second_account.email)
        self.assertTrue(first_account.email.endswith("@example.com"))

    def test_generated_payload_contains_every_documented_field(self) -> None:
        account = create_test_account()

        self.assertEqual(set(ACCOUNT_FIELD_NAMES), set(account.payload))
        self.assertEqual(account.email, account.payload["email"])
        self.assertEqual(account.password, account.payload["password"])

    def test_default_data_is_deterministic_except_for_email(self) -> None:
        first_payload = dict(create_test_account().payload)
        second_payload = dict(create_test_account().payload)
        first_payload.pop("email")
        second_payload.pop("email")

        self.assertEqual(first_payload, second_payload)

    def test_documented_field_overrides_are_applied(self) -> None:
        account = create_test_account(
            {"firstname": "Priya", "city": "Pune", "password": "CustomTestPass123!"}
        )

        self.assertEqual("Priya", account.payload["firstname"])
        self.assertEqual("Pune", account.payload["city"])
        self.assertEqual("CustomTestPass123!", account.password)

    def test_unknown_field_override_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported account field"):
            create_test_account({"role": "admin"})
