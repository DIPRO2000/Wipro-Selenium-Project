"""Reusable assertions for HTTP and JSON API responses."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from requests import Response


def assert_http_status(response: Response, expected_status: int) -> None:
    """Assert that a response has the expected HTTP transport status."""
    actual_status = response.status_code
    if actual_status != expected_status:
        raise AssertionError(
            f"Expected HTTP status {expected_status}, but received {actual_status}."
        )


def get_json_body(response: Response) -> Any:
    """Return a response JSON body or raise a clear assertion error."""
    try:
        return response.json()
    except ValueError as error:
        raise AssertionError("Response body is not valid JSON.") from error


def assert_api_response_code(response: Response, expected_response_code: int) -> None:
    """Assert the AutomationExercise JSON-envelope responseCode field."""
    payload = _get_json_object(response)
    _assert_field_present(payload, "responseCode")
    actual_response_code = payload["responseCode"]
    if actual_response_code != expected_response_code:
        raise AssertionError(
            "Expected API responseCode "
            f"{expected_response_code}, but received {actual_response_code}."
        )


def assert_response_message(response: Response, expected_message: str) -> None:
    """Assert the JSON-envelope message field."""
    payload = _get_json_object(response)
    _assert_field_present(payload, "message")
    actual_message = payload["message"]
    if actual_message != expected_message:
        raise AssertionError(
            f"Expected response message {expected_message!r}, but received {actual_message!r}."
        )


def assert_required_fields(
    payload: Mapping[str, Any], required_fields: Iterable[str]
) -> None:
    """Assert that a JSON-object payload contains each required top-level field."""
    if not isinstance(payload, Mapping):
        raise AssertionError("Response payload must be a JSON object.")

    missing_fields = [field for field in required_fields if field not in payload]
    if missing_fields:
        raise AssertionError(
            "Response payload is missing required fields: " + ", ".join(missing_fields) + "."
        )


def _get_json_object(response: Response) -> Mapping[str, Any]:
    payload = get_json_body(response)
    if not isinstance(payload, Mapping):
        raise AssertionError("Response payload must be a JSON object.")
    return payload


def _assert_field_present(payload: Mapping[str, Any], field_name: str) -> None:
    if field_name not in payload:
        raise AssertionError(f"Response payload is missing required field: {field_name}.")
