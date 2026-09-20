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

**Phase 4 — Response Validation Utilities.** The project now provides a reusable Requests-based client plus validation utilities for HTTP and JSON API responses. Behave scenarios, authentication, live API execution, and Allure reporting integration have not been added yet.

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

Run the Behave suite after feature scenarios are added in a later phase:

```bash
behave
```

## Configuration

Future framework components will read configuration through `config.settings.load_settings()` using standard environment variables. No additional configuration library is required.

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

AutomationExercise can communicate its API outcome in the JSON `responseCode` field, so this validation is intentionally separate from HTTP status validation. The project does not yet include Behave scenarios, authentication, live API execution, or Allure report attachments.
