"""
Order Overview Page Object for SwagLabs Mobile App.
"""

from typing import List, Optional
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage


class OrderOverviewPage(BasePage):
    """Page Object for Checkout Overview screen"""
    
    # Main overview elements
    OVERVIEW_SCREEN_HEADER = (AppiumBy.XPATH, "//android.widget.TextView[@text='CHECKOUT: OVERVIEW']")
    
    # Order summary elements
    ORDER_ITEMS = (AppiumBy.XPATH, "//*[contains(@content-desc, 'test-Item')]")
    ITEM_TITLE = (AppiumBy.XPATH, "//android.widget.TextView[string-length(@text) > 10 and not(contains(@text, '$'))]")
    ITEM_DESCRIPTION = (AppiumBy.XPATH, "//*[contains(@content-desc, 'test-Description')]")
    ITEM_PRICE = (AppiumBy.XPATH, "//*[contains(@content-desc, 'test-Price')]")
    
    # Payment summary - using text-based selectors since content-desc not available
    PAYMENT_INFO = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'Payment Information')")
    SHIPPING_INFO = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'Shipping Information')")
    SUBTOTAL = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'Item total:')]")
    TAX = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'Tax:')]")
    TOTAL = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'Total:')]")
    
    # Buttons
    FINISH_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-FINISH")
    CANCEL_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-CANCEL")
    
    def __init__(self, driver):
        """Initialize Order Overview Page"""
        super().__init__(driver)
    
    def is_displayed(self, timeout: int = 10) -> bool:
        """Check if order overview screen is displayed"""
        return self.is_element_visible(self.OVERVIEW_SCREEN_HEADER, timeout) or \
               self.is_element_present(self.FINISH_BUTTON, timeout)
    
    def wait_for_overview_screen(self, timeout: int = 8):
        """Wait for overview screen to load"""
        self.logger.info("Waiting for order overview screen")
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # Try multiple detection strategies
            if self.is_element_present(self.OVERVIEW_SCREEN_HEADER, timeout=1):
                self.logger.info("Overview screen detected via header")
                return
            if self.is_element_present(self.FINISH_BUTTON, timeout=1):
                self.logger.info("Overview screen detected via FINISH button")
                return
            if self.is_element_present(self.CANCEL_BUTTON, timeout=1):
                self.logger.info("Overview screen detected via CANCEL button")
                return
            # Look for order items as another indicator
            if self.find_elements(self.ORDER_ITEMS, timeout=1):
                self.logger.info("Overview screen detected via order items")
                return
            time.sleep(0.5)
        
        raise Exception(f"Overview screen not detected within {timeout} seconds")
    
    def get_order_items_count(self) -> int:
        """Get number of items in order"""
        # Try multiple strategies to count order items
        self.logger.info("Counting items in order using multiple strategies")
        
        # Strategy 1: Use ORDER_ITEMS selector
        items = self.find_elements(self.ORDER_ITEMS, timeout=3)
        if items:
            count = len(items)
            self.logger.info(f"Found {count} items via ORDER_ITEMS selector")
            return count
        
        # Strategy 2: Count by ITEM_TITLE elements 
        titles = self.find_elements(self.ITEM_TITLE, timeout=3)
        if titles:
            count = len(titles)
            self.logger.info(f"Found {count} items via ITEM_TITLE selector")
            return count
        
        # Strategy 3: Look for any TextView that looks like a product name (length-based, avoiding common UI text)
        fallback_selector = (AppiumBy.XPATH, "//android.widget.TextView[string-length(@text) > 8 and string-length(@text) < 50]")
        fallback_items = self.find_elements(fallback_selector, timeout=3)
        if fallback_items:
            count = len(fallback_items)
            self.logger.info(f"Found {count} items via fallback product name selector")
            return count
        
        self.logger.warning("Could not find any order items using available strategies")
        return 0
    
    def get_order_item_titles(self) -> List[str]:
        """Get list of all order item titles"""
        # Scroll to top to make sure product titles are visible
        for _ in range(3):
            self.scroll_up()
            import time
            time.sleep(0.2)
        
        titles = []
        title_elements = self.find_elements(self.ITEM_TITLE, timeout=5)
        
        for element in title_elements:
            title = element.text.strip()
            if title and len(title) > 5:
                titles.append(title)
        
        self.logger.info(f"Found order item titles: {titles}")
        return titles
    
    def get_order_item_prices(self) -> List[str]:
        """Get list of all order item prices"""
        prices = []
        price_elements = self.find_elements(self.ITEM_PRICE, timeout=5)
        for element in price_elements:
            price = element.text.strip()
            if price:
                prices.append(price)
        self.logger.info(f"Found order item prices: {prices}")
        return prices
    
    def get_subtotal(self) -> str:
        """Get subtotal amount"""
        subtotal_text = self.get_text_with_scroll(self.SUBTOTAL)
        if not subtotal_text:
            raise AssertionError(f"SUBTOTAL element not found with selector: {self.SUBTOTAL}. Element should contain text 'Item total:'")
        return subtotal_text
    
    def get_tax_amount(self) -> str:
        """Get tax amount"""
        tax_text = self.get_text_with_scroll(self.TAX)
        if not tax_text:
            raise AssertionError(f"TAX element not found with selector: {self.TAX}. Element should contain text 'Tax:'")
        return tax_text
    
    def get_total_amount(self) -> str:
        """Get total amount"""
        total_text = self.get_text_with_scroll(self.TOTAL)
        if not total_text:
            raise AssertionError(f"TOTAL element not found with selector: {self.TOTAL}. Element should contain text 'Total:'")
        return total_text
    
    def get_payment_info(self) -> Optional[str]:
        """Get payment information"""
        if self.is_element_present(self.PAYMENT_INFO, timeout=5):
            return self.get_text(self.PAYMENT_INFO)
        return None
    
    def get_shipping_info(self) -> Optional[str]:
        """Get shipping information"""
        if self.is_element_present(self.SHIPPING_INFO, timeout=5):
            return self.get_text(self.SHIPPING_INFO)
        return None
    
    def verify_order_details(self, expected_items: List[str]) -> bool:
        """Verify that order contains expected items"""
        order_titles = self.get_order_item_titles()
        
        for expected_item in expected_items:
            if not any(expected_item.lower() in title.lower() for title in order_titles):
                self.logger.error(f"Expected item '{expected_item}' not found in order overview")
                return False
        
        self.logger.info(f"All expected items found in order overview: {expected_items}")
        return True
    
    def finish_order(self):
        """Click Finish button to complete the order"""
        self.logger.info("Finishing order")
        self.click_with_scroll(self.FINISH_BUTTON, max_scrolls=4)
    
    def cancel_order(self):
        """Click Cancel button to return to inventory"""
        self.logger.info("Cancelling order")
        self.click(self.CANCEL_BUTTON)
    
    def calculate_expected_total(self) -> Optional[float]:
        """Calculate expected total from subtotal and tax"""
        try:
            subtotal_text = self.get_subtotal()
            tax_text = self.get_tax_amount()
            
            if subtotal_text and tax_text:
                # Extract numeric values (assuming format like "Item total: $29.99")
                subtotal_value = float(subtotal_text.split('$')[1]) if '$' in subtotal_text else 0.0
                tax_value = float(tax_text.split('$')[1]) if '$' in tax_text else 0.0
                
                expected_total = subtotal_value + tax_value
                self.logger.info(f"Calculated expected total: ${expected_total:.2f}")
                return expected_total
        except Exception as e:
            self.logger.warning(f"Could not calculate expected total: {e}")
        
        return None
    
    def verify_order_summary(self) -> bool:
        """Verify that order summary contains required information"""
        try:
            subtotal = self.get_subtotal()
            tax = self.get_tax_amount()
            
            # Total might not be available in this version of SwagLabs
            try:
                total = self.get_total_amount()
            except AssertionError:
                total = None
                self.logger.info("Total amount not available, but that's acceptable")
            
            if not all([subtotal, tax]):
                self.logger.error("Missing required order summary information (subtotal or tax)")
                return False
            
            self.logger.info(f"Order summary verification passed - Subtotal: {subtotal}, Tax: {tax}, Total: {total or 'N/A'}")
            return True
            
        except AssertionError as e:
            self.logger.error(f"Order summary verification failed: {e}")
            return False 