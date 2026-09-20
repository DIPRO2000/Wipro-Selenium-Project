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

**Phase 2 — Configuration and Logging.** The project now provides validated environment-based configuration and reusable sanitized logging. API client logic, authentication, response validators, feature scenarios, and step definitions have not been added yet.

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
