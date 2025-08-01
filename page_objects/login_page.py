"""
Login Page Object for SwagLabs Mobile App.
"""

import time
from typing import Optional
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    """Page Object for Login screen"""
    
    # Element locators using accessibility IDs (compatible with existing app)
    LOGIN_SCREEN = (AppiumBy.ACCESSIBILITY_ID, "test-Login")
    USERNAME_INPUT = (AppiumBy.ACCESSIBILITY_ID, "test-Username")
    PASSWORD_INPUT = (AppiumBy.ACCESSIBILITY_ID, "test-Password")
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-LOGIN")
    ERROR_MESSAGE = (AppiumBy.ACCESSIBILITY_ID, "test-Error message")
    
    # Biometry elements
    BIOMETRY_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-biometry")
    
    # Auto-fill user buttons (from original app)
    STANDARD_USER_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-standard_user")
    LOCKED_OUT_USER_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-locked_out_user")
    PROBLEM_USER_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-problem_user") 
    PERFORMANCE_GLITCH_USER_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-performance_glitch_user")
    
    def __init__(self, driver):
        """Initialize Login Page"""
        super().__init__(driver)
    
    def is_displayed(self, timeout: int = 10) -> bool:
        """Check if login screen is displayed"""
        return self.is_element_visible(self.USERNAME_INPUT, timeout)
    
    def wait_for_login_screen(self, timeout: int = 15):
        """Wait for login screen to be displayed"""
        self.logger.info("Waiting for login screen")
        self.wait_for_element(self.USERNAME_INPUT, timeout)
    
    def enter_username(self, username: str):
        """Enter username"""
        self.logger.info(f"Entering username: {username}")
        self.send_keys(self.USERNAME_INPUT, username)
    
    def enter_password(self, password: str):
        """Enter password"""
        self.logger.info("Entering password")
        self.send_keys(self.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """Click login button"""
        self.logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)
    
    def login(self, username: str, password: str):
        """Perform complete login"""
        self.logger.info(f"Logging in with username: {username}")
        self.wait_for_login_screen()
        self.enter_username(username)
        self.enter_password(password)
        self.hide_keyboard()
        self.click_login_button()
        
    def get_error_message(self) -> Optional[str]:
        """Get error message if displayed"""
        if self.is_element_present(self.ERROR_MESSAGE, timeout=5):
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def quick_login_standard_user(self):
        """Quick login with standard user"""
        self.logger.info("Quick login with standard user")
        self.wait_for_login_screen()
        if self.is_element_present(self.STANDARD_USER_BUTTON, timeout=5):
            self.scroll_to_element(self.STANDARD_USER_BUTTON)
            self.click(self.STANDARD_USER_BUTTON)
        else:
            self.login("standard_user", "secret_sauce")
        self.click_login_button()
        
    def quick_login_locked_user(self):
        """Quick login with locked user"""
        self.logger.info("Quick login with locked user")
        self.wait_for_login_screen()
        if self.is_element_present(self.LOCKED_OUT_USER_BUTTON, timeout=5):
            self.scroll_to_element(self.LOCKED_OUT_USER_BUTTON)
            self.click(self.LOCKED_OUT_USER_BUTTON)
        else:
            self.login("locked_out_user", "secret_sauce")
        self.click_login_button()
