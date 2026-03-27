from src.pages.base_page import BasePage


class CalculatorPage(BasePage):
    """Page Object for the Windows Calculator (Standard mode)."""

    # Accessibility IDs for calculator buttons
    _BUTTON_IDS = {
        "0": "num0Button", "1": "num1Button", "2": "num2Button",
        "3": "num3Button", "4": "num4Button", "5": "num5Button",
        "6": "num6Button", "7": "num7Button", "8": "num8Button",
        "9": "num9Button",
        "+": "plusButton", "-": "minusButton",
        "*": "multiplyButton", "/": "divideButton",
        "=": "equalButton", "C": "clearButton", "CE": "clearEntryButton",
    }

    RESULT_DISPLAY_ID = "CalculatorResults"

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def click_button(self, key: str):
        """Click a calculator button by its label (e.g. '1', '+', '=')."""
        automation_id = self._BUTTON_IDS.get(key)
        if not automation_id:
            raise ValueError(f"Unknown calculator key: '{key}'")
        btn = self.wait_for_element_by_id(automation_id)
        self.click(btn)

    def enter_number(self, number: str):
        """Type each digit of a number by clicking individual buttons."""
        for digit in str(number):
            self.click_button(digit)

    def clear(self):
        self.click_button("C")

    def get_result(self) -> str:
        """Return the current display value (strips leading 'Display is ' text if present)."""
        element = self.wait_for_element_by_id(self.RESULT_DISPLAY_ID)
        text = self.get_text(element)
        # Calculator returns text like "Display is 42"
        return text.replace("Display is ", "").strip()

    # ------------------------------------------------------------------
    # High-level helpers
    # ------------------------------------------------------------------

    def calculate(self, num1: str, operator: str, num2: str) -> str:
        """Perform a simple two-operand calculation and return the result string."""
        self.clear()
        self.enter_number(num1)
        self.click_button(operator)
        self.enter_number(num2)
        self.click_button("=")
        return self.get_result()
