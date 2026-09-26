import os
import time
import pytest
from datetime import datetime
from selenium import webdriver


@pytest.fixture
def driver(request):
    """Open Chrome before each test, close after. Screenshot if test fails."""
    d = webdriver.Chrome()
    d.maximize_window()
    d.get("https://www.saucedemo.com/")
    time.sleep(2)

    yield d

    # If the test failed, save a screenshot
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        os.makedirs("screenshots", exist_ok=True)
        path = f"screenshots/{request.node.name}_{datetime.now().strftime('%H%M%S')}.png"
        d.save_screenshot(path)
        print(f"\nScreenshot saved: {path}")

    time.sleep(1)
    d.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook that tells the fixture if the test passed or failed."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
