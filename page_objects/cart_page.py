"""
Cart Page Object for SwagLabs Mobile App.
"""

from typing import List, Optional
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from .base_page import BasePage


class CartPage(BasePage):
    """Page Object for Shopping Cart screen"""
    
    # Main cart elements
    # Try multiple possible cart screen headers since app may vary
    CART_SCREEN_HEADER = (AppiumBy.XPATH, "//android.widget.TextView[@text='YOUR CART' or @text='Cart' or @text='CART']")
    CART_LIST = (AppiumBy.XPATH, "//*[contains(@content-desc, 'test-Cart list')]")
    CONTINUE_SHOPPING_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-CONTINUE SHOPPING")
    CHECKOUT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-CHECKOUT")
    
    # Cart item elements - same as inventory page but may have different context
    CART_ITEM = (AppiumBy.XPATH, "//*[contains(@content-desc, 'test-Item')]")
    CART_ITEM_TITLE = (AppiumBy.XPATH, "//android.widget.TextView[string-length(@text) > 10 and not(contains(@text, '$'))]")
    CART_ITEM_DESCRIPTION = (AppiumBy.XPATH, "//*[contains(@content-desc, 'test-Item desc')]")
    CART_ITEM_PRICE = (AppiumBy.XPATH, "//*[contains(@content-desc, 'test-Price')]")
    REMOVE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-REMOVE")
    
    # Cart quantity and totals
    CART_QUANTITY = (AppiumBy.XPATH, "//*[contains(@content-desc, 'test-Amount')]")
    
    def __init__(self, driver):
        """Initialize Cart Page"""
        super().__init__(driver)
    
    def is_displayed(self, timeout: int = 10) -> bool:
        """Check if cart screen is displayed"""
        return self.is_element_visible(self.CART_SCREEN_HEADER, timeout) or \
               self.is_element_present(self.CHECKOUT_BUTTON, timeout)
    
    def wait_for_cart_screen(self, timeout: int = 8):
        """Wait for cart screen to be displayed"""
        self.logger.info("Waiting for cart screen to load")
        
        # Try multiple ways to detect cart screen since header text may vary
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # Method 1: Try to find header (most reliable when present)
            if self.is_element_present(self.CART_SCREEN_HEADER, timeout=1):
                self.logger.info("Cart screen detected via header")
                return
            
            # Method 2: Look for CHECKOUT button (always present in cart)
            if self.is_element_present(self.CHECKOUT_BUTTON, timeout=1):
                self.logger.info("Cart screen detected via CHECKOUT button")
                return
                
            # Method 3: Look for CONTINUE SHOPPING button  
            if self.is_element_present(self.CONTINUE_SHOPPING_BUTTON, timeout=1):
                self.logger.info("Cart screen detected via CONTINUE SHOPPING button")
                return
            
            time.sleep(0.5)
        
        # If all methods fail, raise timeout
        raise Exception(f"Cart screen not detected within {timeout} seconds")
    
    def get_cart_items_count(self) -> int:
        """Get number of items in cart"""
        # Try to count REMOVE buttons as they indicate items in cart
        remove_buttons = self.find_elements(self.REMOVE_BUTTON, timeout=5)
        if remove_buttons:
            count = len(remove_buttons)
            self.logger.info(f"Found {count} items in cart (based on REMOVE buttons)")
            return count
        
        # Fallback to original item selector
        items = self.find_elements(self.CART_ITEM, timeout=5)
        count = len(items)
        self.logger.info(f"Found {count} items in cart (based on CART_ITEM selector)")
        return count
    
    def get_cart_item_titles(self) -> List[str]:
        """Get list of all cart item titles"""
        titles = []
        title_elements = self.find_elements(self.CART_ITEM_TITLE, timeout=5)
        
        for element in title_elements:
            title = element.text.strip()
            if title and len(title) > 3:
                titles.append(title)
        
        self.logger.info(f"Found cart item titles: {titles}")
        return titles
    
    def get_cart_item_prices(self) -> List[str]:
        """Get list of all cart item prices"""
        prices = []
        price_elements = self.find_elements(self.CART_ITEM_PRICE, timeout=5)
        for element in price_elements:
            price = element.text.strip()
            if price:
                prices.append(price)
        self.logger.info(f"Found cart item prices: {prices}")
        return prices
    
    def is_product_in_cart(self, product_name: str) -> bool:
        """Check if specific product is in cart"""
        cart_titles = self.get_cart_item_titles()
        is_present = any(product_name.lower() in title.lower() for title in cart_titles)
        self.logger.info(f"Product '{product_name}' in cart: {is_present}")
        return is_present
    
    def remove_product_from_cart_by_index(self, index: int):
        """Remove product from cart by index"""
        self.logger.info(f"Removing product {index} from cart")
        
        remove_buttons = self.find_elements(self.REMOVE_BUTTON, timeout=10)
        if index < len(remove_buttons):
            initial_count = len(remove_buttons)
            remove_buttons[index].click()
            self.logger.info(f"Product {index} removed from cart")
            
            # Wait for UI to update (REMOVE button should disappear or change count)
            try:
                # Wait up to 2 seconds for the button count to decrease
                import time
                start_time = time.time()
                while time.time() - start_time < 2:
                    current_buttons = self.find_elements(self.REMOVE_BUTTON, timeout=1)
                    if len(current_buttons) < initial_count:
                        break
                    time.sleep(0.1)  # Small polling interval
            except Exception:
                pass  # Continue even if wait fails
        else:
            raise Exception(f"Remove button at index {index} not found. Only {len(remove_buttons)} REMOVE buttons available")
    
    def remove_product_from_cart_by_name(self, product_name: str):
        """Remove specific product from cart by name"""
        self.logger.info(f"Removing product '{product_name}' from cart")
        
        # Find the product in cart
        cart_titles = self.get_cart_item_titles()
        for i, title in enumerate(cart_titles):
            if product_name.lower() in title.lower():
                self.remove_product_from_cart_by_index(i)
                return
        
        raise Exception(f"Product '{product_name}' not found in cart")
    
    def remove_first_product_from_cart(self):
        """Remove first product from cart"""
        self.logger.info("Removing first product from cart")
        self.remove_product_from_cart_by_index(0)
    
    def clear_cart(self):
        """Remove all products from cart"""
        self.logger.info("Clearing all products from cart")
        
        while True:
            remove_buttons = self.find_elements(self.REMOVE_BUTTON, timeout=3)
            if len(remove_buttons) == 0:
                break
            
            initial_count = len(remove_buttons)
            # Remove first product
            remove_buttons[0].click()
            
            # Wait for UI to update (button should disappear)
            try:
                import time
                start_time = time.time()
                while time.time() - start_time < 2:
                    current_buttons = self.find_elements(self.REMOVE_BUTTON, timeout=1)
                    if len(current_buttons) < initial_count:
                        break
                    time.sleep(0.1)  # Small polling interval
            except Exception:
                pass  # Continue even if wait fails
        
        self.logger.info("Cart cleared successfully")
    
    def continue_shopping(self):
        """Click Continue Shopping button to return to inventory"""
        self.logger.info("Continuing shopping")
        self.click(self.CONTINUE_SHOPPING_BUTTON)
    
    def proceed_to_checkout(self):
        """Click Checkout button to proceed to checkout"""
        self.logger.info("Proceeding to checkout")
        self.click_with_scroll(self.CHECKOUT_BUTTON)
    
    def is_cart_empty(self) -> bool:
        """Check if cart is empty"""
        items_count = self.get_cart_items_count()
        is_empty = items_count == 0
        self.logger.info(f"Cart is empty: {is_empty}")
        return is_empty
    
    def verify_cart_contents(self, expected_products: List[str]) -> bool:
        """Verify that cart contains expected products"""
        cart_titles = self.get_cart_item_titles()
        
        for expected_product in expected_products:
            if not any(expected_product.lower() in title.lower() for title in cart_titles):
                self.logger.error(f"Expected product '{expected_product}' not found in cart")
                return False
        
        self.logger.info(f"All expected products found in cart: {expected_products}")
        return True
    
    def get_total_price(self) -> Optional[str]:
        """Get total price from cart (if displayed)"""
        total_locator = (AppiumBy.XPATH, "//*[contains(@text, 'Total')]")
        if self.is_element_present(total_locator, timeout=3):
            return self.get_text(total_locator)
        return None

