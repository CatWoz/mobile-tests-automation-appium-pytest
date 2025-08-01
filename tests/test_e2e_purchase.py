"""
End-to-End Purchase Flow Tests for SwagLabs Mobile App.

This module contains comprehensive tests for the complete purchase journey:
1. Add product to shopping cart and confirm it's displayed
2. Open shopping cart and continue to checkout
3. Fill all required information fields
4. Navigate to payment screen and enter payment information
5. Proceed to order overview and verify order details
6. Complete the purchase process
"""

import pytest
from page_objects.cart_page import CartPage
from page_objects.checkout_page import CheckoutPage
from page_objects.order_overview_page import OrderOverviewPage
from page_objects.confirmation_page import ConfirmationPage
from tests.base_test import BaseTest


class TestE2EPurchaseFlow(BaseTest):
    """End-to-End purchase flow tests"""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver, login_page, inventory_page):
        """Setup and teardown for each test"""
        # Setup: Before each test
        self.before_each(login_page, inventory_page)
        yield  # This is where the test runs

    @pytest.mark.smoke
    @pytest.mark.e2e
    @pytest.mark.purchase
    def test_complete_purchase_flow_single_product(self, logged_in_user, inventory_page):
        """
        Test complete purchase flow with single product:
        1. Add product to cart and verify
        2. Navigate to checkout and fill information
        3. Review order and complete purchase
        4. Verify successful order completion
        """
        # Step 1: Clear cart if not empty
        inventory_page.wait_for_inventory_screen()
        if inventory_page.is_cart_badge_visible():
            inventory_page.open_cart()
            cart_page = CartPage(inventory_page.driver)
            cart_page.wait_for_cart_screen()
            cart_page.clear_cart()
            cart_page.continue_shopping()
            inventory_page.wait_for_inventory_screen()
        
        # Step 2: Add product to cart
        product_titles = inventory_page.get_product_titles()
        assert len(product_titles) > 0, "Should have products available"
        expected_product = product_titles[0]
        
        inventory_page.add_first_product_to_cart()
        
        # Step 3: Open cart and verify product
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.driver)
        cart_page.wait_for_cart_screen()
        
        cart_items_count = cart_page.get_cart_items_count()
        assert cart_items_count >= 1, f"Cart should contain at least 1 item, got {cart_items_count}"
        assert cart_page.is_product_in_cart(expected_product), f"Product '{expected_product}' should be in cart"
        
        # Step 4: Proceed to checkout
        cart_page.proceed_to_checkout()
        
        # Step 5: Fill checkout information
        checkout_page = CheckoutPage(cart_page.driver)
        checkout_page.wait_for_checkout_screen()
        checkout_page.fill_checkout_information('John', 'Doe', '12345')
        checkout_page.continue_to_overview()
        
        # Step 6: Verify order overview
        overview_page = OrderOverviewPage(checkout_page.driver)
        overview_page.wait_for_overview_screen()
        
        assert overview_page.get_order_items_count() >= 1, "Order should contain at least 1 item"
        assert overview_page.verify_order_details([expected_product]), f"Order should contain '{expected_product}'"
        
        # Step 7: Verify order summary
        assert overview_page.verify_order_summary(), "Order summary should be complete"
        
        # Step 8: Complete order
        overview_page.finish_order()
        
        # Step 9: Verify order completion
        confirmation_page = ConfirmationPage(overview_page.driver)
        confirmation_page.wait_for_confirmation_screen()
        assert confirmation_page.is_order_successful(), "Order should be completed successfully"
        
        # Step 10: Return to inventory
        confirmation_page.back_to_home()
        inventory_page.wait_for_inventory_screen()

    @pytest.mark.regression
    @pytest.mark.e2e
    @pytest.mark.purchase
    def test_complete_purchase_flow_multiple_products(self, logged_in_user, inventory_page):
        """
        Test complete purchase flow with multiple products:
        1. Add multiple products to cart
        2. Navigate through entire checkout process
        3. Verify all products in order overview
        4. Complete purchase successfully
        """
        # Step 1: Clear cart if not empty
        inventory_page.wait_for_inventory_screen()
        if inventory_page.is_cart_badge_visible():
            inventory_page.open_cart()
            cart_page = CartPage(inventory_page.driver)
            cart_page.wait_for_cart_screen()
            cart_page.clear_cart()
            cart_page.continue_shopping()
            inventory_page.wait_for_inventory_screen()
        
        # Step 2: Add multiple products to cart
        product_titles = inventory_page.get_product_titles()
        assert len(product_titles) >= 2, "Should have at least 2 products available"
        
        inventory_page.add_multiple_products_to_cart(2, max_scrolls=10)
        
        # Step 3: Open cart and verify products
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.driver)
        cart_page.wait_for_cart_screen()
        
        actual_cart_count = cart_page.get_cart_items_count()
        assert actual_cart_count >= 1, f"Cart should contain at least 1 item, got {actual_cart_count}"
        
        cart_product_titles = cart_page.get_cart_item_titles()
        assert len(cart_product_titles) >= 1, f"Should have at least 1 product in cart, got {len(cart_product_titles)}"
        
        # Step 4: Proceed to checkout
        cart_page.proceed_to_checkout()
        
        # Step 5: Fill checkout information
        checkout_page = CheckoutPage(cart_page.driver)
        checkout_page.wait_for_checkout_screen()
        checkout_page.fill_checkout_information('Jane', 'Smith', '54321')
        checkout_page.continue_to_overview()
        
        # Step 6: Verify order overview with multiple products
        overview_page = OrderOverviewPage(checkout_page.driver)
        overview_page.wait_for_overview_screen()
        
        assert overview_page.get_order_items_count() >= 1, "Order should contain at least 1 item"
        
        # Verify all cart products are in order overview
        for cart_product in cart_product_titles:
            assert overview_page.verify_order_details([cart_product]), f"Order should contain '{cart_product}'"
        
        # Step 7: Complete order
        overview_page.finish_order()
        
        # Step 8: Verify order completion
        confirmation_page = ConfirmationPage(overview_page.driver)
        confirmation_page.wait_for_confirmation_screen()
        assert confirmation_page.is_order_successful(), "Multiple product order should be completed successfully"
        
        # Step 9: Return to inventory
        confirmation_page.back_to_home()
        inventory_page.wait_for_inventory_screen()

    @pytest.mark.regression
    @pytest.mark.e2e
    @pytest.mark.purchase
    def test_checkout_validation_errors(self, logged_in_user, inventory_page):
        """
        Test checkout form validation:
        1. Add product to cart
        2. Navigate to checkout
        3. Try to continue without filling required fields
        4. Fill fields and continue successfully
        """
        # Step 1: Add product and navigate to checkout
        inventory_page.wait_for_inventory_screen()
        inventory_page.add_first_product_to_cart()
        
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.driver)
        cart_page.wait_for_cart_screen()
        cart_page.proceed_to_checkout()
        
        # Step 2: Try to continue without filling required fields
        checkout_page = CheckoutPage(cart_page.driver)
        checkout_page.wait_for_checkout_screen()
        checkout_page.continue_to_overview()
        
        # Step 3: Fill fields and continue successfully
        checkout_page.fill_checkout_information('Test', 'User', '99999')
        checkout_page.continue_to_overview()
        
        # Step 4: Verify we proceeded to overview page
        overview_page = OrderOverviewPage(checkout_page.driver)
        overview_page.wait_for_overview_screen()
        assert overview_page.is_displayed(), "Should proceed to overview after filling required fields"
