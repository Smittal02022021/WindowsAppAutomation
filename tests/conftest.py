import pytest  # Test framework used for fixtures and hooks
import logging  # Standard library logger for emitting log messages
from src.driver.winapp_driver import create_driver, quit_driver  # Functions to start and stop a WinAppDriver session
from src.utils.logger import setup_logger  # Project-level logger configuration helper
from src.utils.screenshot import take_screenshot  # Utility to save a PNG screenshot from the driver
from config.settings import get_app_path  # Resolves a named app to its path/ID from settings

setup_logger()  # Configure log formatting and output destinations once at import time
logger = logging.getLogger(__name__)  # Module-level logger, named after this file (tests.conftest)


def pytest_configure(config):  # pytest hook called before collection; used here to create required directories
    """Ensure report/log directories exist before the session starts."""
    import os  # Imported here to keep the global namespace clean
    from datetime import datetime  # Used to generate a timestamp for the report filename
    for d in ("reports/screenshots", "logs"):  # Directories needed by screenshot and logger utilities
        os.makedirs(d, exist_ok=True)  # Create the directory (and parents) if it does not already exist
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # e.g. 20260327_153000
    config.option.htmlpath = f"reports/report_{timestamp}.html"  # Each run gets a unique, timestamped report file


@pytest.fixture(scope="function")  # Fixture is created and torn down for each individual test function
def calculator_driver():  # Fixture name matches the parameter name used in tests
    """Launch Windows Calculator, yield driver, quit after test."""
    driver = create_driver(get_app_path("calculator"))  # Open a WinAppDriver session targeting the Calculator app
    yield driver  # Hand the driver to the test; execution pauses here until the test finishes
    quit_driver(driver)  # Teardown: close the Calculator session regardless of pass or fail


@pytest.hookimpl(tryfirst=True, wrapper=True)  # Register as a wrapper hook that runs before other implementations
def pytest_runtest_makereport(item, call):  # Hook called after each test phase (setup / call / teardown)
    """Capture a screenshot on test failure and attach it to the HTML report."""
    report = yield  # Execute the default report-building logic and receive the resulting report object

    if report.when == "call" and report.failed:  # Only act on the actual test body phase when it has failed
        driver = item.funcargs.get("calculator_driver")  # Retrieve the driver fixture from the test's argument list
        if driver:  # Guard against tests that do not use the calculator_driver fixture
            path = take_screenshot(driver, f"FAIL_{item.name}")  # Save a screenshot named after the failing test
            logger.info("Failure screenshot: %s", path)  # Log the saved screenshot path for traceability

            # Attach to pytest-html report
            extras = getattr(report, "extras", [])  # Get any existing extras list, defaulting to empty if absent
            try:
                from pytest_html import extras as html_extras  # Import the pytest-html extras API
                extras.append(html_extras.image(path))  # Embed the screenshot image inline in the HTML report
            except ImportError:  # pytest-html may not be installed in all environments
                pass  # Silently skip attachment if the plugin is unavailable
            report.extras = extras  # Write the updated extras list back onto the report object

    return report  # Return the (possibly augmented) report to pytest
