"""Step definitions for documented login-verification behavior."""

from __future__ import annotations

from behave import given, when
from behave.runner import Context

from framework.account_data import create_test_account
from framework.response_validators import (
    assert_api_response_code,
    assert_http_status,
    assert_response_message,
)


VERIFY_LOGIN_ENDPOINT = "/api/verifyLogin"


@given("a disposable account exists")
def step_disposable_account_exists(context: Context) -> None:
    """Create one unique account for the valid-login scenario."""
    account = create_test_account()
    context.account = account
    context.account_creation_response = context.account_fixture.create(account)
    assert_http_status(context.account_creation_response, 200)
    assert_api_response_code(context.account_creation_response, 201)
    assert_response_message(context.account_creation_response, "User created!")


@when("I verify login with the disposable account credentials")
def step_verify_login_with_disposable_account(context: Context) -> None:
    account = context.account
    context.response = context.api_client.post(
        VERIFY_LOGIN_ENDPOINT,
        data={"email": account.email, "password": account.password},
    )


@when("I verify login with invalid credentials")
def step_verify_login_with_invalid_credentials(context: Context) -> None:
    account = create_test_account(overrides={"password": "WrongPassword123!"})
    context.response = context.api_client.post(
        VERIFY_LOGIN_ENDPOINT,
        data={"email": account.email, "password": account.password},
    )


@when("I verify login without the email parameter")
def step_verify_login_without_email(context: Context) -> None:
    account = create_test_account()
    context.response = context.api_client.post(
        VERIFY_LOGIN_ENDPOINT,
        data={"password": account.password},
    )


@when("I send a DELETE request to the login verification endpoint")
def step_delete_login_verification(context: Context) -> None:
    account = create_test_account()
    context.response = context.api_client.delete(
        VERIFY_LOGIN_ENDPOINT,
        data={"email": account.email, "password": account.password},
    )
