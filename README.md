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

**Phase 1 — Project Setup.** The project structure, dependency configuration, and reporting-ready Behave configuration are in place. API client logic, authentication, response validators, feature scenarios, and step definitions have not been added yet.

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

Copy `.env.example` to `.env` only when configuration loading is introduced in a later phase. Never commit `.env`.
