"""Behavior checks for temporary account setup and cleanup."""

from __future__ import annotations

import unittest
from unittest.mock import Mock

from requests import Response

from framework.account_data import create_test_account
from framework.account_fixture import AccountFixture
from framework.api_client import ApiClient


class AccountFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.api_client = Mock(spec=ApiClient)
        self.account = create_test_account()
        self.fixture = AccountFixture(self.api_client)

    def test_create_delegates_form_data_and_returns_original_response(self) -> None:
        create_response = self._response_with_code(201)
        self.api_client.post.return_value = create_response

        response = self.fixture.create(self.account)

        self.assertIs(create_response, response)
        self.api_client.post.assert_called_once_with(
            "/api/createAccount", data=self.account.payload
        )

    def test_cleanup_deletes_a_created_account_once_and_returns_response(self) -> None:
        self.api_client.post.return_value = self._response_with_code(201)
        delete_response = Mock(spec=Response)
        self.api_client.delete.return_value = delete_response
        self.fixture.create(self.account)

        response = self.fixture.cleanup()

        self.assertIs(delete_response, response)
        self.api_client.delete.assert_called_once_with(
            "/api/deleteAccount",
            data={"email": self.account.email, "password": self.account.password},
        )
        self.assertIsNone(self.fixture.cleanup())
        self.api_client.delete.assert_called_once()

    def test_cleanup_skips_deletion_when_account_creation_never_succeeds(self) -> None:
        self.api_client.post.return_value = self._response_with_code(400)

        self.fixture.create(self.account)

        self.assertIsNone(self.fixture.cleanup())
        self.api_client.delete.assert_not_called()

    def test_cleanup_skips_deletion_when_setup_was_not_attempted(self) -> None:
        self.assertIsNone(self.fixture.cleanup())

        self.api_client.delete.assert_not_called()

    @staticmethod
    def _response_with_code(response_code: int) -> Mock:
        response = Mock(spec=Response)
        response.json.return_value = {"responseCode": response_code}
        return response
