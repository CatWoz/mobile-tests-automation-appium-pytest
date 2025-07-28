"""
Base Page Object class for mobile automation.
Contains common methods used across all page objects.
"""

import time
import logging
from typing import List, Optional, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy


class BasePage:
    """Base page object class with common mobile automation methods"""
    
    def __init__(self, driver):
        """
        Initialize base page with driver instance
        
        Args:
            driver: Appium webdriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.long_wait = WebDriverWait(driver, 30)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    # Element Location Methods
    def find_element(self, locator: Tuple[str, str], timeout: int = 10):
        """
        Find element with explicit wait
        
        Args:
            locator: Tuple of (By method, locator value)
            timeout: Timeout in seconds
            
        Returns:
            WebElement: Found element
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator))
            self.logger.debug(f"Found element: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            self.take_screenshot(f"element_not_found_{int(time.time())}")
            raise
    
    def find_elements(self, locator: Tuple[str, str], timeout: int = 10) -> List:
        """
        Find multiple elements with explicit wait
        
        Args:
            locator: Tuple of (By method, locator value) 
            timeout: Timeout in seconds
            
        Returns:
            List: List of found elements
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            elements = wait.until(EC.presence_of_all_elements_located(locator))
            self.logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            self.logger.warning(f"No elements found: {locator}")
            return []
    
    def find_element_by_accessibility_id(self, accessibility_id: str, timeout: int = 10):
        """
        Find element by accessibility ID (works for both iOS and Android)
        
        Args:
            accessibility_id: Accessibility ID value
            timeout: Timeout in seconds
            
        Returns:
            WebElement: Found element
        """
        locator = (AppiumBy.ACCESSIBILITY_ID, accessibility_id)
        return self.find_element(locator, timeout)
    
    def find_element_by_text(self, text: str, timeout: int = 10):
        """
        Find element by visible text (cross-platform)
        
        Args:
            text: Text to search for
            timeout: Timeout in seconds
            
        Returns:
            WebElement: Found element
        """
        # Try both Android and iOS text selectors
        locators = [
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")'),
            (AppiumBy.IOS_PREDICATE, f'label == "{text}" OR name == "{text}"')
        ]
        
        for locator in locators:
            try:
                return self.find_element(locator, timeout=2)
            except TimeoutException:
                continue
        
        # Fallback to XPath
        xpath_locator = (By.XPATH, f"//*[@text='{text}' or @label='{text}']")
        return self.find_element(xpath_locator, timeout)
    
    # Element Interaction Methods
    def click(self, locator: Tuple[str, str], timeout: int = 10):
        """
        Click on element with wait for clickability
        
        Args:
            locator: Tuple of (By method, locator value)
            timeout: Timeout in seconds
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.debug(f"Clicked element: {locator}")
        except TimeoutException:
            self.logger.error(f"Element not clickable: {locator}")
            self.take_screenshot(f"click_failed_{int(time.time())}")
            raise
    
    def send_keys(self, locator: Tuple[str, str], text: str, clear_first: bool = True, timeout: int = 10):
        """
        Send keys to element
        
        Args:
            locator: Tuple of (By method, locator value)
            text: Text to enter
            clear_first: Whether to clear field first
            timeout: Timeout in seconds
        """
        element = self.find_element(locator, timeout)
        
        if clear_first:
            element.clear()
        
        element.send_keys(text)
        self.logger.debug(f"Sent keys to element: {locator}, text: {text}")
    
    def get_text(self, locator: Tuple[str, str], timeout: int = 10) -> str:
        """
        Get text from element
        
        Args:
            locator: Tuple of (By method, locator value)
            timeout: Timeout in seconds
            
        Returns:
            str: Element text
        """
        element = self.find_element(locator, timeout)
        text = element.text
        self.logger.debug(f"Got text from element: {locator}, text: {text}")
        return text
    
    def get_attribute(self, locator: Tuple[str, str], attribute: str, timeout: int = 10) -> str:
        """
        Get attribute value from element
        
        Args:
            locator: Tuple of (By method, locator value)
            attribute: Attribute name
            timeout: Timeout in seconds
            
        Returns:
            str: Attribute value
        """
        element = self.find_element(locator, timeout)
        value = element.get_attribute(attribute)
        self.logger.debug(f"Got attribute from element: {locator}, attribute: {attribute}, value: {value}")
        return value
    
    # Element State Methods
    def is_element_present(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """
        Check if element is present in DOM
        
        Args:
            locator: Tuple of (By method, locator value)
            timeout: Timeout in seconds
            
        Returns:
            bool: True if element is present
        """
        try:
            self.find_element(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """
        Check if element is visible
        
        Args:
            locator: Tuple of (By method, locator value)
            timeout: Timeout in seconds
            
        Returns:
            bool: True if element is visible
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_clickable(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """
        Check if element is clickable
        
        Args:
            locator: Tuple of (By method, locator value)
            timeout: Timeout in seconds
            
        Returns:
            bool: True if element is clickable
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False
    
    # Wait Methods
    def wait_for_element(self, locator: Tuple[str, str], timeout: int = 10):
        """
        Wait for element to be present
        
        Args:
            locator: Tuple of (By method, locator value)
            timeout: Timeout in seconds
        """
        return self.find_element(locator, timeout)
    
    def wait_for_element_to_disappear(self, locator: Tuple[str, str], timeout: int = 10):
        """
        Wait for element to disappear
        
        Args:
            locator: Tuple of (By method, locator value)
            timeout: Timeout in seconds
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until_not(EC.presence_of_element_located(locator))
            self.logger.debug(f"Element disappeared: {locator}")
        except TimeoutException:
            self.logger.warning(f"Element still present after timeout: {locator}")
    
    # Mobile-specific Actions
    def scroll_down(self, start_x: int = None, start_y: int = None, end_x: int = None, end_y: int = None):
        """
        Scroll down on the screen
        
        Args:
            start_x, start_y, end_x, end_y: Scroll coordinates (optional)
        """
        if not all([start_x, start_y, end_x, end_y]):
            size = self.driver.get_window_size()
            start_x = size['width'] // 2
            start_y = size['height'] * 0.8
            end_x = size['width'] // 2
            end_y = size['height'] * 0.2
        
        self.driver.swipe(start_x, start_y, end_x, end_y, 1000)
        self.logger.debug("Scrolled down")
    
    def scroll_up(self, start_x: int = None, start_y: int = None, end_x: int = None, end_y: int = None):
        """
        Scroll up on the screen
        
        Args:
            start_x, start_y, end_x, end_y: Scroll coordinates (optional)
        """
        if not all([start_x, start_y, end_x, end_y]):
            size = self.driver.get_window_size()
            start_x = size['width'] // 2
            start_y = size['height'] * 0.2
            end_x = size['width'] // 2
            end_y = size['height'] * 0.8
        
        self.driver.swipe(start_x, start_y, end_x, end_y, 1000)
        self.logger.debug("Scrolled up")
    
    def scroll_to_element(self, locator: Tuple[str, str], max_scrolls: int = 5) -> bool:
        """
        Scroll until element is found
        
        Args:
            locator: Element locator
            max_scrolls: Maximum number of scroll attempts
            
        Returns:
            bool: True if element was found
        """
        for i in range(max_scrolls):
            if self.is_element_present(locator, timeout=2):
                self.logger.debug(f"Found element after {i} scrolls: {locator}")
                return True
            self.scroll_down()
        
        self.logger.warning(f"Element not found after {max_scrolls} scrolls: {locator}")
        return False
    
    def tap_at_coordinates(self, x: int, y: int):
        """
        Tap at specific coordinates
        
        Args:
            x, y: Coordinates to tap
        """
        self.driver.tap([(x, y)], 100)
        self.logger.debug(f"Tapped at coordinates: ({x}, {y})")
    
    # App Management
    def background_app(self, seconds: int = 3):
        """
        Put app in background for specified time
        
        Args:
            seconds: Time to keep app in background
        """
        self.driver.background_app(seconds)
        self.logger.debug(f"App backgrounded for {seconds} seconds")
    
    def restart_app(self):
        """Restart the application"""
        self.driver.reset()
        self.logger.debug("App restarted")
    
    def close_app(self):
        """Close the application"""
        self.driver.close_app()
        self.logger.debug("App closed")
    
    def launch_app(self):
        """Launch the application"""
        self.driver.launch_app()
        self.logger.debug("App launched")
    
    # Utility Methods
    def take_screenshot(self, filename: str = None) -> str:
        """
        Take screenshot and save to reports directory
        
        Args:
            filename: Screenshot filename (without extension)
            
        Returns:
            str: Path to saved screenshot
        """
        if not filename:
            filename = f"screenshot_{int(time.time())}"
        
        # Create screenshots directory
        from pathlib import Path
        screenshots_dir = Path(__file__).parent.parent / "reports" / "screenshots"
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = screenshots_dir / f"{filename}.png"
        self.driver.save_screenshot(str(filepath))
        self.logger.info(f"Screenshot saved: {filepath}")
        return str(filepath)
    
    def get_page_source(self) -> str:
        """
        Get current page source
        
        Returns:
            str: Page source XML
        """
        return self.driver.page_source
    
    def get_current_activity(self) -> str:
        """
        Get current Android activity (Android only)
        
        Returns:
            str: Current activity name
        """
        if self.driver.capabilities.get('platformName', '').lower() == 'android':
            return self.driver.current_activity
        return ""
    
    def wait_for_activity(self, activity: str, timeout: int = 10):
        """
        Wait for specific Android activity (Android only)
        
        Args:
            activity: Activity name to wait for
            timeout: Timeout in seconds
        """
        if self.driver.capabilities.get('platformName', '').lower() == 'android':
            self.driver.wait_activity(activity, timeout)
    
    def hide_keyboard(self):
        """Hide keyboard if present"""
        try:
            self.driver.hide_keyboard()
            self.logger.debug("Keyboard hidden")
        except Exception:
            self.logger.debug("No keyboard to hide")
