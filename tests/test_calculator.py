import pytest  # Test framework for writing and running tests
from tests.pages.calculator_page import CalculatorPage  # Page object for the Windows Calculator app


@pytest.fixture  # Marks this function as a pytest fixture (shared setup for tests)
def calc(calculator_driver):  # Receives the driver fixture defined in conftest.py
    return CalculatorPage(calculator_driver)  # Wraps the driver in the CalculatorPage page object


class TestCalculatorAddition:  # Groups all addition-related test cases
    def test_add_two_positive_numbers(self, calc):  # Verifies 8 + 3 = 11
        result = calc.calculate("8", "+", "3")  # Performs the calculation via the UI
        assert result == "11", f"Expected 11, got {result}"  # Asserts the displayed result matches expected value

    def test_add_zero(self, calc):  # Verifies adding zero leaves the number unchanged
        result = calc.calculate("7", "+", "0")  # Performs 7 + 0 via the UI
        assert result == "7", f"Expected 7, got {result}"  # Asserts result is still 7


class TestCalculatorSubtraction:  # Groups all subtraction-related test cases
    def test_subtract_smaller_from_larger(self, calc):  # Verifies 9 - 4 = 5
        result = calc.calculate("9", "-", "4")  # Performs the calculation via the UI
        assert result == "5", f"Expected 5, got {result}"  # Asserts the displayed result matches expected value


class TestCalculatorMultiplication:  # Groups all multiplication-related test cases
    def test_multiply_two_numbers(self, calc):  # Verifies 6 * 7 = 42
        result = calc.calculate("6", "*", "7")  # Performs the calculation via the UI
        assert result == "42", f"Expected 42, got {result}"  # Asserts the displayed result matches expected value

    def test_multiply_by_zero(self, calc):  # Verifies any number multiplied by zero equals zero
        result = calc.calculate("9", "*", "0")  # Performs 9 * 0 via the UI
        assert result == "0", f"Expected 0, got {result}"  # Asserts result is 0


class TestCalculatorDivision:  # Groups all division-related test cases
    def test_divide_evenly(self, calc):  # Verifies 8 / 2 = 4
        result = calc.calculate("8", "/", "2")  # Performs the calculation via the UI
        assert result == "4", f"Expected 4, got {result}"  # Asserts the displayed result matches expected value
