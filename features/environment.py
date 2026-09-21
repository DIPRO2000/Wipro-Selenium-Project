"""Behave hooks for isolated API scenarios and disposable account cleanup."""

from __future__ import annotations

from behave.runner import Context

from config.settings import load_settings
from framework.account_fixture import AccountFixture
from framework.api_client import ApiClient


def before_scenario(context: Context, scenario: object) -> None:
    """Create an isolated configured API client for each scenario."""
    context.api_client = ApiClient(settings=load_settings())
    context.account_fixture = AccountFixture(context.api_client)
    context.response = None


def after_scenario(context: Context, scenario: object) -> None:
    """Clean up any disposable account, then close the Requests session."""
    account_fixture = getattr(context, "account_fixture", None)
    if account_fixture is not None:
        account_fixture.cleanup()

    api_client = getattr(context, "api_client", None)
    if api_client is not None:
        api_client.session.close()
