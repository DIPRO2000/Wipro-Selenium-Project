"""Behavior checks for reusable response validation utilities."""

from __future__ import annotations

import unittest
from unittest.mock import Mock

import requests

from framework.response_validators import (
    assert_api_response_code,
    assert_http_status,
    assert_required_fields,
    assert_response_message,
    get_json_body,
)


class ResponseValidatorTests(unittest.TestCase):
    def _response(self, status_code: int = 200, payload: object | None = None) -> Mock:
        response = Mock(spec=requests.Response)
        response.status_code = status_code
        response.json.return_value = {} if payload is None else payload
        return response

    def test_matching_http_status_passes(self) -> None:
        assert_http_status(self._response(status_code=200), 200)

    def test_mismatched_http_status_has_expected_and_actual_values(self) -> None:
        with self.assertRaisesRegex(
            AssertionError, "Expected HTTP status 200, but received 404"
        ):
            assert_http_status(self._response(status_code=404), 200)

    def test_get_json_body_returns_parsed_response_body(self) -> None:
        payload = {"responseCode": 200, "message": "User exists!"}

        self.assertEqual(payload, get_json_body(self._response(payload=payload)))

    def test_get_json_body_rejects_invalid_json(self) -> None:
        response = self._response()
        response.json.side_effect = ValueError("invalid JSON")

        with self.assertRaisesRegex(AssertionError, "Response body is not valid JSON"):
            get_json_body(response)

    def test_matching_api_response_code_passes(self) -> None:
        assert_api_response_code(self._response(payload={"responseCode": 201}), 201)

    def test_missing_api_response_code_is_reported(self) -> None:
        with self.assertRaisesRegex(AssertionError, "missing required field: responseCode"):
            assert_api_response_code(self._response(payload={}), 200)

    def test_mismatched_api_response_code_has_expected_and_actual_values(self) -> None:
        with self.assertRaisesRegex(
            AssertionError, "Expected API responseCode 200, but received 400"
        ):
            assert_api_response_code(self._response(payload={"responseCode": 400}), 200)

    def test_matching_response_message_passes(self) -> None:
        assert_response_message(
            self._response(payload={"message": "User created!"}), "User created!"
        )

    def test_missing_response_message_is_reported(self) -> None:
        with self.assertRaisesRegex(AssertionError, "missing required field: message"):
            assert_response_message(self._response(payload={}), "User created!")

    def test_mismatched_response_message_has_expected_and_actual_values(self) -> None:
        with self.assertRaisesRegex(
            AssertionError, "Expected response message 'User created!', but received 'User not found!'"
        ):
            assert_response_message(
                self._response(payload={"message": "User not found!"}), "User created!"
            )

    def test_required_fields_pass_when_present(self) -> None:
        assert_required_fields(
            {"responseCode": 200, "products": []}, ["responseCode", "products"]
        )

    def test_missing_required_fields_are_reported(self) -> None:
        with self.assertRaisesRegex(
            AssertionError, "Response payload is missing required fields: products, brands"
        ):
            assert_required_fields({"responseCode": 200}, ["products", "brands"])
