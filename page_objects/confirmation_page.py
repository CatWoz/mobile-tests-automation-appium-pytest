"""
Confirmation Page Object for SwagLabs Mobile App.
"""

from typing import Optional
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage


class ConfirmationPage(BasePage):
    """Page Object for Order Confirmation screen"""
    
    # Main confirmation elements
    CONFIRMATION_HEADER = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'CHECKOUT') and contains(@text, 'COMPLETE')]")
    SUCCESS_MESSAGE = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'THANK YOU')]")
    ORDER_COMPLETE_TEXT = (AppiumBy.XPATH, "//*[contains(@text, 'order') and contains(@text, 'complete')]")
    
    # Success icon/image
    SUCCESS_ICON = (AppiumBy.XPATH, "//*[@content-desc='test-checkout-complete-icon']")
    PONY_EXPRESS_IMAGE = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Pony Express')]")
    
    # Buttons
    BACK_HOME_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-BACK HOME")
    
    def __init__(self, driver):
        """Initialize Confirmation Page"""
        super().__init__(driver)
    
    def is_displayed(self, timeout: int = 10) -> bool:
        """Check if confirmation screen is displayed"""
        return self.is_element_visible(self.CONFIRMATION_HEADER, timeout) and \
               self.is_element_present(self.SUCCESS_MESSAGE, timeout) and \
               self.is_element_present(self.BACK_HOME_BUTTON, timeout)
    
    def wait_for_confirmation_screen(self, timeout: int = 5):
        """Wait for confirmation screen to load"""
        self.logger.info("Waiting for order confirmation screen")
        self.wait_for_element(self.CONFIRMATION_HEADER, timeout)
    
    def is_order_successful(self) -> bool:
        """Check if order was completed successfully"""
        # Check required elements for successful order
        self.assert_element_present(self.CONFIRMATION_HEADER, timeout=5, 
                                   error_msg="Order completion failed - CONFIRMATION_HEADER ('CHECKOUT: COMPLETE!') not found")
        self.assert_element_present(self.SUCCESS_MESSAGE, timeout=2,
                                   error_msg="Order completion failed - SUCCESS_MESSAGE ('THANK YOU FOR YOU ORDER') not found") 
        self.assert_element_present(self.BACK_HOME_BUTTON, timeout=2,
                                   error_msg="Order completion failed - BACK_HOME_BUTTON ('test-BACK HOME') not found")
        
        self.logger.info("Order completed successfully - all required elements present")
        return True
    
    def get_confirmation_header(self) -> Optional[str]:
        """Get confirmation header text"""
        if self.is_element_present(self.CONFIRMATION_HEADER, timeout=5):
            return self.get_text(self.CONFIRMATION_HEADER)
        return None
    
    def get_success_message(self) -> Optional[str]:
        """Get success message text"""
        if self.is_element_present(self.SUCCESS_MESSAGE, timeout=5):
            return self.get_text(self.SUCCESS_MESSAGE)
        return None
    
    def get_order_complete_text(self) -> Optional[str]:
        """Get order complete description text"""
        if self.is_element_present(self.ORDER_COMPLETE_TEXT, timeout=5):
            return self.get_text(self.ORDER_COMPLETE_TEXT)
        return None
    
    def is_success_icon_displayed(self) -> bool:
        """Check if success icon is displayed"""
        # Check both required icon elements
        self.assert_element_present(self.SUCCESS_ICON, timeout=5,
                                   error_msg="Success icon failed - SUCCESS_ICON not found")
        self.assert_element_present(self.PONY_EXPRESS_IMAGE, timeout=5,
                                   error_msg="Success icon failed - PONY_EXPRESS_IMAGE not found")
        
        self.logger.info("Success icon displayed - all elements present")
        return True
    
    def back_to_home(self):
        """Click Back Home button to return to inventory"""
        self.logger.info("Returning to home/inventory screen")
        self.click(self.BACK_HOME_BUTTON)
    
    def verify_order_completion(self) -> bool:
        """Verify that order was completed successfully"""
        try:
            # Check all success indicators
            header_ok = self.get_confirmation_header() is not None
            message_ok = self.get_success_message() is not None
            button_ok = self.is_element_present(self.BACK_HOME_BUTTON, timeout=3)
            
            completion_verified = header_ok and message_ok and button_ok
            
            if completion_verified:
                self.logger.info("Order completion verified successfully")
            else:
                self.logger.error("Order completion verification failed")
            
            return completion_verified
            
        except Exception as e:
            self.logger.error(f"Order completion verification error: {e}")
            return False
    
    def get_all_confirmation_elements(self) -> dict:
        """Get all available confirmation elements for debugging"""
        elements = {
            'header': self.get_confirmation_header(),
            'success_message': self.get_success_message(),
            'order_complete_text': self.get_order_complete_text(),
            'success_icon_present': self.is_success_icon_displayed(),
            'back_button_present': self.is_element_present(self.BACK_HOME_BUTTON, timeout=3)
        }
        
        self.logger.info(f"Confirmation elements: {elements}")
        return elements 