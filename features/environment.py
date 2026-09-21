"""Behave hooks for isolated API scenarios and disposable account cleanup."""

from __future__ import annotations

from behave.runner import Context

from config.settings import load_settings
from framework.account_fixture import AccountFixture
from framework.api_client import ApiClient
from framework.allure_utils import attach_http_exchange


def before_scenario(context: Context, scenario: object) -> None:
    """Create an isolated configured API client for each scenario."""
    context.api_client = ApiClient(settings=load_settings())
    context.account_fixture = AccountFixture(context.api_client)
    context.response = None
    context._allure_attached_response_ids = set()


def after_step(context: Context, step: object) -> None:
    """Attach each request-producing step's exchange once, when available."""
    response = getattr(context, "response", None)
    if response is None:
        response = getattr(context, "account_creation_response", None)
    api_client = getattr(context, "api_client", None)
    request = getattr(api_client, "last_request", None)
    if response is None or request is None:
        return

    attached_response_ids = getattr(context, "_allure_attached_response_ids", set())
    response_id = id(response)
    if response_id in attached_response_ids:
        return

    attach_http_exchange(request, response)
    attached_response_ids.add(response_id)


def after_scenario(context: Context, scenario: object) -> None:
    """Clean up any disposable account, then close the Requests session."""
    account_fixture = getattr(context, "account_fixture", None)
    if account_fixture is not None:
        cleanup_response = account_fixture.cleanup()
        api_client = getattr(context, "api_client", None)
        request = getattr(api_client, "last_request", None)
        if cleanup_response is not None and request is not None:
            attach_http_exchange(request, cleanup_response, name_prefix="Account cleanup")

    api_client = getattr(context, "api_client", None)
    if api_client is not None:
        api_client.session.close()
