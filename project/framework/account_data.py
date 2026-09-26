"""Disposable account data for future API scenarios."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from uuid import uuid4


ACCOUNT_FIELD_NAMES = (
    "name",
    "email",
    "password",
    "title",
    "birth_date",
    "birth_month",
    "birth_year",
    "firstname",
    "lastname",
    "company",
    "address1",
    "address2",
    "country",
    "zipcode",
    "state",
    "city",
    "mobile_number",
)

_DEFAULT_ACCOUNT_FIELDS = {
    "name": "Automation Test User",
    "password": "TrainingTestPass123!",
    "title": "Mr",
    "birth_date": "1",
    "birth_month": "January",
    "birth_year": "1990",
    "firstname": "Automation",
    "lastname": "User",
    "company": "Training Project",
    "address1": "123 Test Street",
    "address2": "Test District",
    "country": "United States",
    "zipcode": "10001",
    "state": "New York",
    "city": "New York",
    "mobile_number": "1234567890",
}


@dataclass(frozen=True)
class TestAccount:
    """A disposable account and its form-data payload."""

    email: str
    password: str
    payload: Mapping[str, str]


def create_test_account(overrides: Mapping[str, str] | None = None) -> TestAccount:
    """Create a documented AutomationExercise account payload with a unique email."""
    values = {**_DEFAULT_ACCOUNT_FIELDS, "email": _generate_unique_email()}
    if overrides:
        _validate_override_fields(overrides)
        values.update(overrides)

    return TestAccount(
        email=values["email"],
        password=values["password"],
        payload=MappingProxyType(values),
    )


def _generate_unique_email() -> str:
    return f"api-training-{uuid4().hex}@example.com"


def _validate_override_fields(overrides: Mapping[str, str]) -> None:
    unsupported_fields = set(overrides).difference(ACCOUNT_FIELD_NAMES)
    if unsupported_fields:
        unsupported_list = ", ".join(sorted(unsupported_fields))
        raise ValueError(f"Unsupported account field override: {unsupported_list}.")
