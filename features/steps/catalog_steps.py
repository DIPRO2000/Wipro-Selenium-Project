"""Step definitions for catalog API scenarios."""

from __future__ import annotations

from collections.abc import Mapping
import re

from behave import given, then, when
from behave.runner import Context

from framework.response_validators import (
    assert_api_response_code,
    assert_http_status,
    assert_required_fields,
    assert_response_message,
    get_json_body,
)


PRODUCTS_ENDPOINT = "/api/productsList"
BRANDS_ENDPOINT = "/api/brandsList"
SEARCH_ENDPOINT = "/api/searchProduct"


@given("the API client is configured")
def step_api_client_is_configured(context: Context) -> None:
    if not hasattr(context, "api_client"):
        raise AssertionError("The Behave environment did not configure an API client.")


@when("I request the all products list")
def step_request_all_products(context: Context) -> None:
    context.response = context.api_client.get(PRODUCTS_ENDPOINT)


@when("I request the all brands list")
def step_request_all_brands(context: Context) -> None:
    context.response = context.api_client.get(BRANDS_ENDPOINT)


@when('I search products for "{search_term}"')
def step_search_products(context: Context, search_term: str) -> None:
    context.response = context.api_client.post(
        SEARCH_ENDPOINT,
        data={"search_product": search_term},
    )


@when("I search products without a search term")
def step_search_products_without_term(context: Context) -> None:
    context.response = context.api_client.post(SEARCH_ENDPOINT, data={})


@then("the HTTP status should be {expected_status:d}")
def step_http_status(context: Context, expected_status: int) -> None:
    assert_http_status(context.response, expected_status)


@then("the API response code should be {expected_response_code:d}")
def step_api_response_code(context: Context, expected_response_code: int) -> None:
    assert_api_response_code(context.response, expected_response_code)


@then('the response should contain a non-empty "{field_name}" list')
def step_non_empty_response_list(context: Context, field_name: str) -> None:
    payload = get_json_body(context.response)
    assert_required_fields(payload, [field_name])
    values = payload[field_name]
    if not isinstance(values, list) or not values:
        raise AssertionError(f"Response field {field_name!r} must be a non-empty list.")


@then('each item in the "{field_name}" list should contain fields {fields}')
def step_list_items_have_fields(context: Context, field_name: str, fields: str) -> None:
    payload = get_json_body(context.response)
    assert_required_fields(payload, [field_name])
    values = payload[field_name]
    if not isinstance(values, list) or not values:
        raise AssertionError(f"Response field {field_name!r} must be a non-empty list.")

    required_fields = re.findall(r'"([^"]+)"', fields)
    if not required_fields:
        raise AssertionError("At least one quoted required field must be provided.")
    for index, item in enumerate(values):
        if not isinstance(item, Mapping):
            raise AssertionError(
                f"Item {index} in response field {field_name!r} must be an object."
            )
        try:
            assert_required_fields(item, required_fields)
        except AssertionError as error:
            raise AssertionError(
                f"Item {index} in response field {field_name!r} is invalid: {error}"
            ) from error


@then('the response message should be "{expected_message}"')
def step_response_message(context: Context, expected_message: str) -> None:
    assert_response_message(context.response, expected_message)
