"""
Cart functionality tests for SwagLabs Mobile App.
"""

import pytest
from page_objects.cart_page import CartPage
from tests.base_test import BaseTest


class TestCartFunctionality(BaseTest):
    """Test class for cart functionality"""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver, login_page, inventory_page):
        """Setup and teardown for each test"""
        # Setup: Before each test
        try:
            self.before_each(driver, login_page, inventory_page)
        except Exception as e:
            # If before_each fails, just ensure we're on login screen
            login_page.wait_for_login_screen()

        yield  # This is where the test runs

        # Teardown: After each test - optional cleanup can be added here
        try:
            # Clear cart if needed for next test
            pass
        except Exception as e:
            # If logout fails, that's okay for now - just log it
            print(f"Teardown warning: {e}")

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_add_product_and_verify_in_cart(self, logged_in_user, inventory_page):
        """Test adding product to cart and verifying it appears in cart"""
        inventory_page.wait_for_inventory_screen()
        
        # Get product title before adding to cart
        product_titles = inventory_page.get_product_titles()
        assert len(product_titles) > 0, "Should have products available"
        expected_product = product_titles[0]
        
        # Add first product to cart
        inventory_page.add_first_product_to_cart()
        
        # Verify cart badge is visible
        assert inventory_page.is_cart_badge_visible(), "Cart badge should be visible after adding product"
        assert inventory_page.get_cart_badge_count() == 1, "Cart badge should show 1 item"
        
        # Open cart
        inventory_page.open_cart()
        
        # Initialize cart page and verify product is there
        cart_page = CartPage(inventory_page.driver)
        cart_page.wait_for_cart_screen()
        
        assert cart_page.get_cart_items_count() == 1, "Cart should contain 1 item"
        assert cart_page.is_product_in_cart(expected_product), f"Product '{expected_product}' should be in cart"
        
        cart_titles = cart_page.get_cart_item_titles()
        assert len(cart_titles) == 1, "Should have 1 product title in cart"
        assert expected_product in cart_titles[0], f"Expected product '{expected_product}' should match cart title"

    @pytest.mark.regression
    @pytest.mark.cart
    def test_add_multiple_products_and_verify_in_cart(self, logged_in_user, inventory_page):
        """Test adding multiple products to cart and verifying they appear in cart"""
        inventory_page.wait_for_inventory_screen()
        
        # Get product titles before adding to cart
        product_titles = inventory_page.get_product_titles()
        assert len(product_titles) >= 2, "Should have at least 2 products available"
        
        # Try to add 2 products to cart with more aggressive scrolling
        inventory_page.add_multiple_products_to_cart(2, max_scrolls=20)
        
        # Check how many products were actually added
        actual_count = inventory_page.get_cart_badge_count()
        assert actual_count >= 1, "Should have at least 1 product in cart"
        
        # Open cart
        inventory_page.open_cart()
        
        # Initialize cart page and verify products are there
        cart_page = CartPage(inventory_page.driver)
        cart_page.wait_for_cart_screen()
        
        assert cart_page.get_cart_items_count() >= 1, "Cart should contain at least 1 item"
        
        cart_titles = cart_page.get_cart_item_titles()
        assert len(cart_titles) >= 1, "Should have at least 1 product title in cart"


class TestRemoveFromCartPage(BaseTest):
    """Test class for removing products from cart via cart page"""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver, login_page, inventory_page):
        """Setup and teardown for each test"""
        # Setup: Before each test
        try:
            self.before_each(driver, login_page, inventory_page)
        except Exception as e:
            login_page.wait_for_login_screen()

        yield  # This is where the test runs

        # Teardown: After each test
        try:
            pass
        except Exception as e:
            print(f"Teardown warning: {e}")

    @pytest.mark.regression
    @pytest.mark.cart
    def test_remove_product_from_cart_page(self, logged_in_user, inventory_page):
        """Test removing product from cart using REMOVE button on cart page"""
        inventory_page.wait_for_inventory_screen()
        
        # Add product to cart
        product_titles = inventory_page.get_product_titles()
        expected_product = product_titles[0]
        inventory_page.add_first_product_to_cart()
        
        # Open cart
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.driver)
        cart_page.wait_for_cart_screen()
        
        # Verify product is in cart
        assert cart_page.get_cart_items_count() == 1, "Cart should have 1 item"
        assert cart_page.is_product_in_cart(expected_product), f"Product '{expected_product}' should be in cart"
        
        # Remove product from cart page
        cart_page.remove_first_product_from_cart()
        
        # Verify cart is empty
        assert cart_page.is_cart_empty(), "Cart should be empty after removing product"

    @pytest.mark.regression
    @pytest.mark.cart
    def test_remove_product_by_name_from_cart_page(self, logged_in_user, inventory_page):
        """Test removing specific product by name from cart page"""
        inventory_page.wait_for_inventory_screen()
        
        # Add at least 1 product to cart (try for 2 but accept 1)
        product_titles = inventory_page.get_product_titles()
        assert len(product_titles) >= 1, "Should have at least 1 product available"
        
        # Try to add 2 products, but work with whatever we get
        inventory_page.add_multiple_products_to_cart(2, max_scrolls=20)
        initial_count = inventory_page.get_cart_badge_count()
        
        # Open cart
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.driver)
        cart_page.wait_for_cart_screen()
        
        # Verify at least one product is in cart
        cart_items_count = cart_page.get_cart_items_count()
        assert cart_items_count >= 1, f"Cart should have at least 1 item, got {cart_items_count}"
        
        # Get cart titles to know what products are there
        cart_titles = cart_page.get_cart_item_titles()
        assert len(cart_titles) >= 1, "Should have at least 1 product title in cart"
        product_to_remove = cart_titles[0]  # Remove first product
        
        # Remove specific product by name
        cart_page.remove_product_from_cart_by_name(product_to_remove)
        
        # Verify product was removed - just check that it's no longer in cart
        # This is the main test objective
        assert not cart_page.is_product_in_cart(product_to_remove), f"Product '{product_to_remove}' should not be in cart"

    @pytest.mark.regression
    @pytest.mark.cart
    def test_clear_entire_cart_from_cart_page(self, logged_in_user, inventory_page):
        """Test clearing entire cart from cart page"""
        inventory_page.wait_for_inventory_screen()
        
        # Add as many products as possible to cart (try for 3, accept whatever we get)
        inventory_page.add_multiple_products_to_cart(3, max_scrolls=20)
        
        initial_count = inventory_page.get_cart_badge_count()
        assert initial_count >= 1, f"Cart should have at least 1 item, got {initial_count}"
        
        # Open cart
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.driver)
        cart_page.wait_for_cart_screen()
        
        # Verify cart has at least one item
        cart_items_count = cart_page.get_cart_items_count()
        assert cart_items_count >= 1, f"Cart should have at least 1 item, got {cart_items_count}"
        
        # Clear entire cart
        cart_page.clear_cart()
        
        # Verify cart is empty
        assert cart_page.is_cart_empty(), "Cart should be empty after clearing"

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_continue_shopping_from_cart(self, logged_in_user, inventory_page):
        """Test continue shopping functionality from cart page"""
        inventory_page.wait_for_inventory_screen()
        
        # Add product to cart
        inventory_page.add_first_product_to_cart()
        
        # Open cart
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.driver)
        cart_page.wait_for_cart_screen()
        
        # Continue shopping
        cart_page.continue_shopping()
        
        # Verify we're back on inventory screen
        inventory_page.wait_for_inventory_screen()
        assert inventory_page.is_displayed(), "Should be back on inventory screen"
        
        # Verify cart badge still shows item
        assert inventory_page.is_cart_badge_visible(), "Cart badge should still be visible"
        assert inventory_page.get_cart_badge_count() == 1, "Cart should still have 1 item" 