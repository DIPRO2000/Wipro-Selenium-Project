"""Temporary account setup and cleanup built on the generic API client."""

from __future__ import annotations

from collections.abc import Mapping

from requests import Response

from framework.account_data import TestAccount
from framework.api_client import ApiClient


CREATE_ACCOUNT_ENDPOINT = "/api/createAccount"
DELETE_ACCOUNT_ENDPOINT = "/api/deleteAccount"


class AccountFixture:
    """Create one disposable account and clean it up at most once."""

    def __init__(self, api_client: ApiClient) -> None:
        self._api_client = api_client
        self._account: TestAccount | None = None
        self._cleanup_required = False

    def create(self, account: TestAccount) -> Response:
        """Create an account and register it for cleanup only after API success."""
        response = self._api_client.post(CREATE_ACCOUNT_ENDPOINT, data=account.payload)
        if _account_was_created(response):
            self._account = account
            self._cleanup_required = True
        return response

    def cleanup(self) -> Response | None:
        """Delete the registered account once, returning its original response."""
        if not self._cleanup_required or self._account is None:
            return None

        account = self._account
        self._cleanup_required = False
        self._account = None
        return self._api_client.delete(
            DELETE_ACCOUNT_ENDPOINT,
            data={"email": account.email, "password": account.password},
        )


def _account_was_created(response: Response) -> bool:
    try:
        payload = response.json()
    except ValueError:
        return False
    return isinstance(payload, Mapping) and payload.get("responseCode") == 201
