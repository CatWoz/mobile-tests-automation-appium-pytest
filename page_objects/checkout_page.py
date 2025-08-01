"""
Checkout Page Object for SwagLabs Mobile App.
"""

from typing import Optional
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object for Checkout Information screen"""
    
    # Main checkout elements
    CHECKOUT_SCREEN_HEADER = (AppiumBy.XPATH, "//android.widget.TextView[@text='CHECKOUT: INFORMATION']")
    
    # Input fields
    FIRST_NAME_INPUT = (AppiumBy.ACCESSIBILITY_ID, "test-First Name")
    LAST_NAME_INPUT = (AppiumBy.ACCESSIBILITY_ID, "test-Last Name")
    POSTAL_CODE_INPUT = (AppiumBy.ACCESSIBILITY_ID, "test-Zip/Postal Code")
    
    # Buttons
    CONTINUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-CONTINUE")
    CANCEL_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-CANCEL")
    
    # Error elements
    ERROR_MESSAGE = (AppiumBy.XPATH, "//*[contains(@content-desc, 'test-Error message')]")
    
    def __init__(self, driver):
        """Initialize Checkout Page"""
        super().__init__(driver)
    
    def is_displayed(self, timeout: int = 10) -> bool:
        """Check if checkout screen is displayed"""
        return self.is_element_visible(self.CHECKOUT_SCREEN_HEADER, timeout)
    
    def wait_for_checkout_screen(self, timeout: int = 8):
        """Wait for checkout screen to load"""
        self.logger.info("Waiting for checkout screen")
        self.wait_for_element(self.CHECKOUT_SCREEN_HEADER, timeout)
    
    def enter_first_name(self, first_name: str):
        """Enter first name"""
        self.logger.info(f"Entering first name: {first_name}")
        self.send_keys(self.FIRST_NAME_INPUT, first_name)
    
    def enter_last_name(self, last_name: str):
        """Enter last name"""
        self.logger.info(f"Entering last name: {last_name}")
        self.send_keys(self.LAST_NAME_INPUT, last_name)
    
    def enter_postal_code(self, postal_code: str):
        """Enter postal code"""
        self.logger.info(f"Entering postal code: {postal_code}")
        self.send_keys(self.POSTAL_CODE_INPUT, postal_code)
    
    def fill_checkout_information(self, first_name: str, last_name: str, postal_code: str):
        """Fill all checkout information fields"""
        self.logger.info("Filling checkout information")
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
    
    def continue_to_overview(self):
        """Click Continue button to proceed to overview"""
        self.logger.info("Proceeding to overview")
        
        # CONTINUE button is visible after filling form - click directly
        self.click(self.CONTINUE_BUTTON)
    
    def cancel_checkout(self):
        """Click Cancel button to return to cart"""
        self.logger.info("Cancelling checkout")
        self.click(self.CANCEL_BUTTON)
    
    def get_error_message(self) -> Optional[str]:
        """Get error message if present"""
        if self.is_element_present(self.ERROR_MESSAGE, timeout=3):
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def is_error_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self.is_element_present(self.ERROR_MESSAGE, timeout=3)
    
    def get_first_name_value(self) -> str:
        """Get current value of first name field"""
        return self.get_attribute(self.FIRST_NAME_INPUT, "text")
    
    def get_last_name_value(self) -> str:
        """Get current value of last name field"""
        return self.get_attribute(self.LAST_NAME_INPUT, "text")
    
    def get_postal_code_value(self) -> str:
        """Get current value of postal code field"""
        return self.get_attribute(self.POSTAL_CODE_INPUT, "text")
    
    def clear_all_fields(self):
        """Clear all input fields"""
        self.logger.info("Clearing all checkout fields")
        
        # Clear first name
        first_name_element = self.find_element(self.FIRST_NAME_INPUT)
        first_name_element.clear()
        
        # Clear last name
        last_name_element = self.find_element(self.LAST_NAME_INPUT)
        last_name_element.clear()
        
        # Clear postal code
        postal_code_element = self.find_element(self.POSTAL_CODE_INPUT)
        postal_code_element.clear() 