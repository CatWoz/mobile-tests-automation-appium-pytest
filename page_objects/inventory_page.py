"""
Inventory Page Object for SwagLabs Mobile App.
"""

from typing import List, Optional
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from .base_page import BasePage


class InventoryPage(BasePage):
    """Page Object for Inventory/Products screen"""
    
    # Main screen elements
    PRODUCTS_SCREEN_HEADER = (AppiumBy.XPATH, "//android.widget.TextView[@text='PRODUCTS']")
    MENU_BUTTON = (AppiumBy.XPATH, "//*[contains(@content-desc, 'test-Menu')]")
    CART_BUTTON = (AppiumBy.XPATH, "//*[contains(@content-desc, 'test-Cart')]")    
    CART_BADGE = (AppiumBy.XPATH, "//android.widget.TextView[@text and string-length(@text) > 0 and number(@text) = number(@text)]")
    
    # Sorting
    SORT_BUTTON = (AppiumBy.XPATH, "//*[contains(@content-desc, 'test-Modal Selector Button')]")
    
    # Menu elements
    LOGOUT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-LOGOUT")
    LOGIN_SCREEN = (AppiumBy.ACCESSIBILITY_ID, "test-Login")
    
    # Product elements (generic patterns)
    PRODUCT_ITEM = (AppiumBy.XPATH, "//*[contains(@content-desc, 'test-Item')]")
    PRODUCT_TITLE = (AppiumBy.XPATH, "//*[contains(@content-desc, 'test-Item title')]")
    PRODUCT_PRICE = (AppiumBy.XPATH, "//*[contains(@content-desc, 'test-Price')]")
    ADD_TO_CART_BUTTON = (AppiumBy.XPATH, "//*[contains(@content-desc, 'test-ADD TO CART')]")
    REMOVE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-REMOVE")
    
    # Specific product locators (by index or name)
    FIRST_PRODUCT = (By.XPATH, "//*[contains(@content-desc, 'test-Item')]")
    SECOND_PRODUCT = (By.XPATH, "//*[contains(@content-desc, 'test-Item-1')]")
    
    # Sort modal options
    SORT_MODAL = (AppiumBy.XPATH, "//*[contains(@text, 'Sort Items by...')]")
    SORT_NAME_ASC = (AppiumBy.XPATH, "//*[contains(@text, 'Name (A to Z)')]")
    SORT_NAME_DESC = (AppiumBy.XPATH, "//*[contains(@text, 'Name (Z to A)')]")
    SORT_PRICE_ASC = (AppiumBy.XPATH, "//*[contains(@text, 'Price (low to high)')]")
    SORT_PRICE_DESC = (AppiumBy.XPATH, "//*[contains(@text, 'Price (high to low)')]")
    
    def __init__(self, driver):
        """Initialize Inventory Page"""
        super().__init__(driver)
    
    def is_displayed(self, timeout: int = 10) -> bool:
        """Check if inventory screen is displayed"""
        return self.is_element_visible(self.PRODUCTS_SCREEN_HEADER, timeout) or \
               self.is_element_present(self.MENU_BUTTON, timeout)
    
    def wait_for_inventory_screen(self, timeout: int = 15):
        """Wait for inventory screen to load"""
        self.logger.info("Waiting for inventory screen")
        self.wait_for_element(self.PRODUCTS_SCREEN_HEADER, timeout)
        # Also wait for products to be loaded
        self.wait_for_element(self.PRODUCT_ITEM, timeout=5)
    
    def get_products_count(self) -> int:
        """Get number of products displayed on current screen"""
        products = self.find_elements(self.PRODUCT_ITEM, timeout=5)
        count = len(products)
        self.logger.info(f"Found {count} products on screen")
        return count
    
    def get_total_products_count_with_scrolling(self, max_scrolls: int = 10) -> int:
        """Get total number of products by scrolling through the entire inventory"""
        self.logger.info("Counting all products with scrolling")
        all_product_titles = set()  # Use set to avoid counting duplicates
        consecutive_empty_scrolls = 0
        max_consecutive_empty = 3
        
        # Start from top
        for _ in range(3):  # Scroll up a few times to ensure we're at the top
            self.scroll_up()
            import time
            time.sleep(0.3)
        
        while consecutive_empty_scrolls < max_consecutive_empty:
            # Get current products
            current_products = self.find_elements(self.PRODUCT_TITLE, timeout=2)
            
            if len(current_products) > 0:
                # Add product titles to our set
                for product in current_products:
                    try:
                        title = product.text.strip()
                        if title:
                            all_product_titles.add(title)
                    except Exception:
                        continue
                consecutive_empty_scrolls = 0
            else:
                consecutive_empty_scrolls += 1
            
            # Scroll down to see more products
            self.scroll_down()
            import time
            time.sleep(0.5)
        
        total_count = len(all_product_titles)
        self.logger.info(f"Found {total_count} total unique products in inventory")
        return total_count
    
    def get_product_titles(self) -> List[str]:
        """Get list of all product titles"""
        titles = []
        title_elements = self.find_elements(self.PRODUCT_TITLE, timeout=5)
        for element in title_elements:
            try:
                title = element.text
                if title:
                    titles.append(title)
            except Exception:
                continue
        self.logger.info(f"Found product titles: {titles}")
        return titles
    
    def get_product_prices(self) -> List[str]:
        """Get list of all product prices"""
        prices = []
        price_elements = self.find_elements(self.PRODUCT_PRICE, timeout=5)
        for element in price_elements:
            try:
                price = element.text
                if price:
                    prices.append(price)
            except Exception:
                continue
        self.logger.info(f"Found product prices: {prices}")
        return prices
    
    def add_first_product_to_cart(self):
        """Add first product to cart"""
        self.logger.info("Adding first product to cart")
        self.add_product_to_cart_by_index(0)
    
    def add_product_to_cart_by_index(self, index: int, max_scrolls: int = 5):
        """Add product to cart by index (0-based) with scrolling support"""
        self.logger.info(f"Adding product at position {index} to cart")
        
        # Try to find the product with scrolling if necessary
        scroll_attempts = 0
        
        while scroll_attempts <= max_scrolls:
            # Get current available ADD TO CART buttons
            add_buttons = self.find_elements(self.ADD_TO_CART_BUTTON, timeout=2)
            self.logger.info(f"Found {len(add_buttons)} available ADD TO CART buttons (scroll attempt {scroll_attempts})")
            
            if index < len(add_buttons):
                # Found the product at the requested index
                add_buttons[index].click()
                self.logger.info(f"Product at position {index} added to cart")
                # Brief wait for UI to update
                import time
                time.sleep(0.3)
                return
            
            # Product not found at current position, try scrolling down
            if scroll_attempts < max_scrolls:
                self.logger.info(f"Product at index {index} not visible, scrolling down (attempt {scroll_attempts + 1})")
                self.scroll_down()
                scroll_attempts += 1
                # Brief wait for scroll animation
                import time
                time.sleep(0.5)
            else:
                break
        
        # If we get here, we couldn't find the product even after scrolling
        final_buttons = self.find_elements(self.ADD_TO_CART_BUTTON, timeout=2)
        raise Exception(f"Cannot add product at position {index} after {max_scrolls} scrolls. Only {len(final_buttons)} ADD TO CART buttons available")
    
    def add_multiple_products_to_cart(self, count: int, max_scrolls: int = 10):
        """Add multiple products to cart sequentially with scrolling support"""
        self.logger.info(f"Adding {count} products to cart")
        added_count = 0
        scroll_attempts = 0
        
        while added_count < count and scroll_attempts < max_scrolls:
            # Find available ADD TO CART buttons
            add_buttons = self.find_elements(self.ADD_TO_CART_BUTTON, timeout=2)
            
            if len(add_buttons) > 0:
                # Add the first available product
                add_buttons[0].click()
                added_count += 1
                self.logger.info(f"Added product {added_count} of {count} to cart")
                
                # Brief wait for UI to update
                import time
                time.sleep(0.3)
                
                # Reset scroll attempts since we found a product
                scroll_attempts = 0
            else:
                # No ADD TO CART buttons visible, try scrolling to find more products
                self.logger.info(f"No ADD TO CART buttons visible, scrolling to find more products (attempt {scroll_attempts + 1})")
                self.scroll_down()
                scroll_attempts += 1
                
                # Brief wait for scroll animation
                import time
                time.sleep(0.5)
        
        if added_count < count:
            self.logger.warning(f"Could only add {added_count} out of {count} requested products after scrolling")
        else:
            self.logger.info(f"Successfully added all {count} products to cart")
    
    def add_all_available_products_to_cart(self, max_scrolls: int = 20):
        """Add all available products to cart by scrolling through the entire inventory"""
        self.logger.info("Adding all available products to cart")
        added_count = 0
        consecutive_empty_scrolls = 0
        max_consecutive_empty = 3  # Stop if we scroll 3 times without finding new products
        
        while consecutive_empty_scrolls < max_consecutive_empty and added_count < 50:  # Safety limit
            # Find available ADD TO CART buttons
            add_buttons = self.find_elements(self.ADD_TO_CART_BUTTON, timeout=2)
            
            if len(add_buttons) > 0:
                # Add all visible products
                current_batch = len(add_buttons)
                for button in add_buttons:
                    try:
                        button.click()
                        added_count += 1
                        self.logger.info(f"Added product {added_count} to cart")
                        
                        # Brief wait for UI to update
                        import time
                        time.sleep(0.2)
                    except Exception as e:
                        self.logger.warning(f"Failed to add product: {e}")
                        continue
                
                consecutive_empty_scrolls = 0
            else:
                consecutive_empty_scrolls += 1
                self.logger.info(f"No ADD TO CART buttons visible, scrolling down (empty scroll {consecutive_empty_scrolls})")
            
            # Scroll down to find more products
            self.scroll_down()
            import time
            time.sleep(0.5)
        
        self.logger.info(f"Added {added_count} products to cart total")
        return added_count
    
    def add_product_to_cart_by_name(self, product_name: str):
        """Add specific product to cart by name"""
        self.logger.info(f"Adding product '{product_name}' to cart")
        
        # Scroll to find the product
        if self.scroll_to_product(product_name):
            # Find the add to cart button for this specific product
            product_xpath = f"//*[contains(@content-desc, 'test-{product_name}')]//following-sibling::*[contains(@content-desc, 'test-ADD TO CART')]"
            add_button = (By.XPATH, product_xpath)
            
            if self.is_element_present(add_button, timeout=5):
                self.click(add_button)
                self.logger.info(f"Product '{product_name}' added to cart")
            else:
                raise Exception(f"Add to cart button not found for product '{product_name}'")
        else:
            raise Exception(f"Product '{product_name}' not found")
    
    def remove_product_from_cart_by_index(self, index: int):
        """Remove product from cart by index"""
        self.logger.info(f"Removing product {index} from cart")
        
        remove_buttons = self.find_elements(self.REMOVE_BUTTON, timeout=10)
        if index < len(remove_buttons):
            remove_buttons[index].click()
            self.logger.info(f"Product {index} removed from cart")
        else:
            raise Exception(f"Remove button at index {index} not found. Only {len(remove_buttons)} REMOVE buttons available")
    
    def click_product_by_index(self, index: int):
        """Click on product to view details"""
        self.logger.info(f"Clicking on product {index}")
        
        products = self.find_elements(self.PRODUCT_ITEM, timeout=10)
        if index < len(products):
            products[index].click()
            self.logger.info(f"Clicked on product {index}")
        else:
            raise Exception(f"Product at index {index} not found")
    
    def scroll_to_product(self, product_name: str, max_scrolls: int = 5) -> bool:
        """Scroll to find specific product"""
        self.logger.info(f"Scrolling to find product: {product_name}")
        
        for i in range(max_scrolls):
            # Check if product is visible
            product_locator = (By.XPATH, f"//*[contains(@content-desc, '{product_name}') or contains(@text, '{product_name}')]")
            if self.is_element_present(product_locator, timeout=2):
                self.logger.info(f"Found product '{product_name}' after {i} scrolls")
                return True
            
            # Scroll down to see more products
            self.scroll_down()
        
        self.logger.warning(f"Product '{product_name}' not found after {max_scrolls} scrolls")
        return False
    
    def open_sort_menu(self):
        """Open sorting options menu"""
        self.logger.info("Opening sort menu")
        self.click(self.SORT_BUTTON)
    
    def sort_by_name_ascending(self):
        """Sort products by name A to Z using XPath"""
        self.logger.info("Sorting products by name A to Z")
        
        # Open sort menu
        self.click(self.SORT_BUTTON)
        
        # Select option
        self.click(self.SORT_NAME_ASC)
        
        # Wait for products to reload after sorting
        self.wait_for_element(self.PRODUCT_ITEM, timeout=2)
    
    def sort_by_name_descending(self):
        """Sort products by name Z-A"""
        self.logger.info("Sorting by name Z-A")
        self.open_sort_menu()
        self.click(self.SORT_NAME_DESC)
    
    def sort_by_price_ascending(self):
        """Sort products by price low to high"""
        self.logger.info("Sorting by price low to high")
        self.open_sort_menu()
        self.click(self.SORT_PRICE_ASC)
    
    def sort_by_price_descending(self):
        """Sort products by price high to low"""
        self.logger.info("Sorting by price high to low")
        self.open_sort_menu()
        self.click(self.SORT_PRICE_DESC)
    

    def open_menu(self):
        """Open hamburger menu"""
        self.logger.info("Opening menu")
        self.click(self.MENU_BUTTON)
    
    def open_cart(self):
        """Open shopping cart"""
        self.logger.info("Opening cart")
        self.click(self.CART_BUTTON)
    
    def get_cart_badge_count(self) -> Optional[int]:
        """Get number from cart badge. Returns None if badge is not visible (empty cart)"""
        try:
            if self.is_element_present(self.CART_BADGE, timeout=2):
                badge_text = self.get_text(self.CART_BADGE).strip()
                if badge_text.isdigit():
                    return int(badge_text)
        except Exception:
            pass
        return None
    
    def is_cart_badge_visible(self) -> bool:
        """Check if cart badge is visible (indicating items in cart). 
        Returns False for empty cart, True when cart has items."""
        return self.is_element_present(self.CART_BADGE, timeout=2)
    
    def wait_for_cart_badge_to_appear(self, timeout: int = 5):
        """Wait for cart badge to appear (when adding first item to cart)"""
        self.wait_for_element(self.CART_BADGE, timeout)
    
    def wait_for_cart_badge_to_disappear(self, timeout: int = 5):
        """Wait for cart badge to disappear (when cart becomes empty)"""
        self.wait_for_element_to_disappear(self.CART_BADGE, timeout)
    
    def wait_for_cart_badge_count(self, expected_count: int, timeout: int = 5) -> bool:
        """Wait for cart badge to show specific count.
        For expected_count=0, waits for badge to disappear.
        For expected_count>0, waits for badge to appear with correct count."""
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.verify_product_added_to_cart(expected_count):
                return True
            time.sleep(0.5)
        
        return False
    
    def wait_for_products_to_load(self, timeout: int = 15):
        """Wait for products to be loaded on screen"""
        self.logger.info("Waiting for products to load")
        self.wait_for_element(self.PRODUCT_ITEM, timeout)
    
    def verify_product_added_to_cart(self, expected_count: int = 1) -> bool:
        """Verify product was added to cart by checking badge.
        For expected_count=0, verifies badge is not visible (empty cart).
        For expected_count>0, verifies badge shows correct count."""
        actual_count = self.get_cart_badge_count()
        return (expected_count == 0 and actual_count is None) or (actual_count == expected_count)
    
    def get_all_add_to_cart_buttons_count(self) -> int:
        """Get count of all 'Add to Cart' buttons visible"""
        buttons = self.find_elements(self.ADD_TO_CART_BUTTON, timeout=5)
        count = len(buttons)
        self.logger.info(f"Found {count} 'Add to Cart' buttons")
        return count
    
    def get_all_remove_buttons_count(self) -> int:
        """Get count of all 'Remove' buttons visible"""
        buttons = self.find_elements(self.REMOVE_BUTTON, timeout=5)
        count = len(buttons)
        self.logger.info(f"Found {count} 'Remove' buttons")
        return count 
    
    def logout(self):
        """Logout from the app"""
        self.logger.info("Logging out")
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_BUTTON)
        assert self.is_element_present(self.LOGIN_SCREEN, timeout=5), "Login screen not found after logout"
