# Wipro Selenium Training Capstone

This repository contains the Selenium and API automation assignments completed during Wipro training. The work demonstrates browser automation, test frameworks, data-driven testing, reusable page objects, BDD-style scenarios, Robot Framework automation, API validation, and reporting.

## Repository Contents

### Selenium Training Assignments

The assignments use SauceDemo as the browser automation application under test.

| Module | Focus | Documentation |
| --- | --- | --- |
| Module 2 | Unittest, PyTest, fixtures, data-driven testing, POM, and HTML reporting | [Module 2 README](assignments/module_2/README.md) |
| Module 3 | Selenium with BDD-style scenarios, data-driven testing, and POM | [Module 3 README](assignments/module_3/README.md) |
| Module 4 | Robot Framework, SeleniumLibrary, custom Python keywords, tags, and reporting | [Module 4 README](assignments/module_4/README.md) |

The `assignments/module_1` directory is reserved for the earlier training module.

### API Automation Capstone

The [`project`](project/README.md) folder contains a separate REST API automation framework for the AutomationExercise API. It uses:

- Python and Requests
- Behave BDD
- Reusable API client and response validators
- Disposable test-account setup and cleanup
- Allure reporting

## Environment Setup

Activate the Conda environment used for the assignments:

```powershell
conda activate selenium_env
```

Install the Selenium assignment dependencies:

```powershell
python -m pip install selenium pytest pytest-html robotframework robotframework-seleniumlibrary
```

Install the API project dependencies:

```powershell
cd project
python -m pip install -r requirements.txt
```

## Running the Work

Run Module 2:

```powershell
cd assignments/module_2
python assignment7.py
python assignment8.py
python -m pytest assignment9.py -v --html=report.html --self-contained-html
```

Run Module 3:

```powershell
cd assignments/module_3
python assignment1.py
python assignment2.py
python assignment3.py
```

Run Module 4:

```powershell
cd assignments/module_4
python -m robot -d results assignment1_basics.robot
python -m robot -d results assignment2_advanced.robot
```

Run the API capstone:

```powershell
cd project
python -m unittest discover -s tests -v
python -m behave --dry-run
python -m behave
```

## Evidence and Reports

Assignment screenshots are stored in each module's `screenshots` folder. The API capstone's final submission evidence is stored in [`project/Output`](project/Output), including the Allure PDF, terminal output, and screenshots.

Generated caches, raw Allure results, and regenerable reports are excluded through the project-specific `.gitignore` files.
