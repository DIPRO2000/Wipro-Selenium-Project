"""Behave hooks for the catalog API scenarios."""

from __future__ import annotations

from behave.runner import Context

from config.settings import load_settings
from framework.api_client import ApiClient


def before_scenario(context: Context, scenario: object) -> None:
    """Create an isolated configured API client for each scenario."""
    context.api_client = ApiClient(settings=load_settings())
    context.response = None


def after_scenario(context: Context, scenario: object) -> None:
    """Close the scenario's reusable Requests session."""
    api_client = getattr(context, "api_client", None)
    if api_client is not None:
        api_client.session.close()
