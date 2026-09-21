# Python API Automation Framework

## Purpose

This REST API automation framework is being created for the Selenium/API Automation Training Capstone. It will test APIs directly; Selenium or browser automation is not part of this project.

## Technology stack

- Python
- Requests
- Behave BDD
- Allure

## API under test

[AutomationExercise API documentation](https://automationexercise.com/api_list)

## Current status

**Phase 9 — Refactoring and Cleanup.** The catalog, authentication, validation, account-fixture, and Allure foundations are implemented. This phase keeps the framework maintainable and removes generated artifacts without adding new API behavior.

## Planned architecture

```text
Feature → Step Definition → API Client → Requests → API → Validation → Allure
```

## Setup

Create and activate a project-local virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the Behave suite:

```bash
behave
```

## Configuration

Framework components read configuration through `config.settings.load_settings()` using standard environment variables. No additional configuration library is required.

| Variable | Default | Purpose |
| --- | --- | --- |
| `BASE_URL` | `https://automationexercise.com` | Base URL for the API under test |
| `REQUEST_TIMEOUT` | `30` seconds | Positive timeout value for future HTTP requests |
| `LOG_LEVEL` | `INFO` | Python logging level, such as `DEBUG`, `INFO`, `WARNING`, or `ERROR` |

Configuration values are validated when loaded. An empty base URL, non-positive or non-numeric timeout, and invalid log level raise a clear `ValueError`.

`.env.example` documents the expected variables. Copy it to `.env` only when a later phase introduces configuration-file loading; `.env` is intentionally ignored by Git and must never contain committed credentials.

## Logging and sensitive data

`framework.logging_utils` configures console logging and file logging at `logs/api_automation.log`. Generated logs are ignored by Git.

Use `log_sanitized()` for request-like data. It recursively redacts values for sensitive keys, including `password`, `Authorization`, `token`, `access_token`, and `refresh_token`, replacing their values with `***REDACTED***`. Do not log raw credentials or tokens.

## API client

`framework.api_client.ApiClient` is the shared HTTP boundary for future framework components. It uses a reusable `requests.Session`, reads the configured base URL and timeout, and provides `get`, `post`, `put`, and `delete` methods for relative endpoints.

The client accepts query parameters, form data, JSON data, and request headers. It returns the original `requests.Response` without response validation or authentication behavior. Each request logs sanitized metadata, so sensitive form, JSON, and header values remain redacted.

## Response validation

`framework.response_validators` provides small reusable assertions for future Behave steps. It validates HTTP transport status codes, parses JSON response bodies, checks AutomationExercise JSON-envelope `responseCode` values, checks response messages, and verifies required top-level response fields.

AutomationExercise can communicate its API outcome in the JSON `responseCode` field, so this validation is intentionally separate from HTTP status validation. The project uses these validators in the catalog and authentication Behave scenarios.

## Catalog API scenarios

`features/catalog.feature` covers the documented catalog endpoints:

- `GET /api/productsList`
- `GET /api/brandsList`
- `POST /api/searchProduct` with `search_product=top`
- `POST /api/searchProduct` without the required parameter

The step definitions call `ApiClient` and the shared response validators. They do not contain direct Requests calls or endpoint-specific response parsing outside the reusable framework layer.

## Account test-data foundation

`framework.account_data` creates documented AutomationExercise account form data with a unique email per account. `framework.account_fixture` delegates account creation and one-time cleanup to the shared `ApiClient`, registering cleanup only after the API reports `responseCode: 201`.

The authentication feature uses these helpers only for valid-login setup and cleanup. Broader account creation/update/lookup/delete scenarios remain future work.

## Authentication API scenarios

`features/authentication.feature` covers the documented login-verification endpoint, `POST /api/verifyLogin`, with four Behave scenarios:

- valid credentials from a disposable account
- an unregistered email and invalid password
- a request missing the email parameter
- the documented unsupported `DELETE` method

AutomationExercise verifies credentials through the JSON response envelope; it does not issue bearer tokens or use OAuth. The valid-login scenario creates a unique temporary account through `AccountFixture`, verifies the credentials, and deletes the account during the scenario cleanup hook. No raw Requests calls or credentials are placed in feature files.

Full account lifecycle coverage remains future work.

## Refactoring and cleanup

`ApiClient.close()` owns release of the reusable Requests session, so Behave hooks do not reach into the session implementation directly. Generated logs, Allure results/reports, Python caches, and local configuration remain excluded from Git; `.gitkeep` files preserve the intended directories.

## Allure reporting

Behave is configured with `allure_behave.formatter:AllureFormatter`, writing result files to `allure-results/`. Request and response exchanges are attached through `framework.allure_utils` with sensitive fields redacted using the existing sanitization rules. Passwords, authorization values, and tokens are never attached in raw form.

If the external Allure command-line tool is installed, generate an HTML report with:

```bash
allure generate allure-results -o allure-report --clean
```

Generated result and report files are ignored by Git. The Python `allure-behave` dependency creates compatible result files; rendering the HTML report requires the separate Allure CLI.
