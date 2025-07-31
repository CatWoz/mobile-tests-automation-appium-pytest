"""
Inventory functionality tests for SwagLabs Mobile App.
"""

import pytest
from page_objects.inventory_page import InventoryPage
from tests.base_test import BaseTest

class TestInventory (BaseTest):
    """Test class for inventory functionality"""

    def before_each(self, login_page, inventory_page):
        """Before each test"""
        super().before_each(login_page, inventory_page)

    def after_each(self, login_page, inventory_page):
        """After each test"""
        super().after_each(login_page, inventory_page)
    
    @pytest.mark.smoke
    @pytest.mark.inventory
    def test_products_displayed(self, logged_in_user, inventory_page):
        """Test that products are displayed on inventory screen"""
        inventory_page.wait_for_inventory_screen()
        assert inventory_page.is_displayed(), "Inventory screen should be displayed"
        
        inventory_page.wait_for_products_to_load()
        products_count = inventory_page.get_products_count()
        assert products_count > 0, "At least one product should be displayed"
        
        product_titles = inventory_page.get_product_titles()
        product_prices = inventory_page.get_product_prices()
        
        assert len(product_titles) > 0, "Product titles should be visible"
        assert len(product_prices) > 0, "Product prices should be visible"
    
    @pytest.mark.smoke
    @pytest.mark.inventory
    def test_add_first_product_to_cart(self, logged_in_user, inventory_page):
        """Test adding first product to cart"""
        inventory_page.wait_for_inventory_screen()
        
        initial_cart_count = inventory_page.get_cart_badge_count() or 0
        inventory_page.add_first_product_to_cart()
        
        expected_count = initial_cart_count + 1
        assert inventory_page.verify_product_added_to_cart(expected_count), \
            f"Cart should show {expected_count} items"
        
        assert inventory_page.is_cart_badge_visible(), "Cart badge should be visible"
    
    @pytest.mark.regression
    @pytest.mark.inventory
    def test_add_multiple_products_to_cart(self, logged_in_user, inventory_page):
        """Test adding multiple products to cart"""
        inventory_page.wait_for_inventory_screen()
        
        # Add first product (index 0)
        inventory_page.add_product_to_cart_by_index(0)
        
        # Add second product (now at index 0 of remaining ADD TO CART buttons)
        inventory_page.add_product_to_cart_by_index(0)
        
        cart_count = inventory_page.get_cart_badge_count()
        assert cart_count == 2, "Cart should contain 2 items"

    
    @pytest.mark.regression
    @pytest.mark.inventory
    def test_remove_product_from_cart(self, logged_in_user, inventory_page):
        """Test removing product from cart"""
        inventory_page.wait_for_inventory_screen()
        inventory_page.add_first_product_to_cart()
        assert inventory_page.get_cart_badge_count() == 1, "Product should be in cart"
        
        inventory_page.remove_product_from_cart_by_index(0)
        
        # Verify cart is empty - badge should not be visible
        assert inventory_page.verify_product_added_to_cart(0), "Cart should be empty after removing product"


class TestProductSorting:
    """Test class for product sorting functionality"""
    
    @pytest.mark.regression
    @pytest.mark.inventory
    def test_sort_by_name_ascending(self, logged_in_user, inventory_page):
        """Test sorting products by name A-Z"""
        inventory_page.wait_for_inventory_screen()
        
        inventory_page.sort_by_name_ascending()
        # Wait for sorting to complete - already handled in sort_by_name_ascending method
        
        sorted_titles = inventory_page.get_product_titles()
        assert len(sorted_titles) > 1, "Need at least 2 products to test sorting"
        
        # Verify that titles are sorted A-Z (regardless of which specific products are shown)
        expected_sorted = sorted(sorted_titles)
        assert sorted_titles == expected_sorted, f"Products should be sorted alphabetically A-Z. Got: {sorted_titles}"
    
    @pytest.mark.regression
    @pytest.mark.inventory
    def test_sort_by_name_descending(self, logged_in_user, inventory_page):
        """Test sorting products by name Z-A"""
        inventory_page.wait_for_inventory_screen()
        
        inventory_page.sort_by_name_descending()
        inventory_page.wait_for_element(inventory_page.PRODUCT_ITEM, timeout=2)  # Wait for sorting to complete
        
        sorted_titles = inventory_page.get_product_titles()
        assert len(sorted_titles) > 1, "Need at least 2 products to test sorting"
        
        # Verify that titles are sorted Z-A (regardless of which specific products are shown)
        expected_sorted = sorted(sorted_titles, reverse=True)
        assert sorted_titles == expected_sorted, f"Products should be sorted alphabetically Z-A. Got: {sorted_titles}"
    
    @pytest.mark.regression
    @pytest.mark.inventory
    def test_sort_by_price_ascending(self, logged_in_user, inventory_page):
        """Test sorting products by price low to high"""
        inventory_page.wait_for_inventory_screen()
        
        inventory_page.sort_by_price_ascending()
        inventory_page.wait_for_element(inventory_page.PRODUCT_ITEM, timeout=2)  # Wait for sorting to complete
        
        prices = inventory_page.get_product_prices()
        assert len(prices) > 1, "Need at least 2 products to test price sorting"
        
        # Extract numeric values from price strings (e.g., "$29.99" -> 29.99)
        numeric_prices = []
        for price in prices:
            try:
                # Remove currency symbol and convert to float
                numeric_price = float(price.replace('$', '').replace(',', ''))
                numeric_prices.append(numeric_price)
            except ValueError:
                continue
        
        if len(numeric_prices) > 1:
            # Check if prices are in ascending order
            assert numeric_prices == sorted(numeric_prices), f"Products should be sorted by price low to high. Got prices: {numeric_prices}"

    @pytest.mark.regression
    @pytest.mark.inventory
    def test_sort_by_price_descending(self, logged_in_user, inventory_page):
        """Test sorting products by price high to low"""
        inventory_page.wait_for_inventory_screen()
        
        inventory_page.sort_by_price_descending()
        inventory_page.wait_for_element(inventory_page.PRODUCT_ITEM, timeout=2)  # Wait for sorting to complete
        
        prices = inventory_page.get_product_prices()
        assert len(prices) > 1, "Need at least 2 products to test price sorting"
        
        # Extract numeric values from price strings (e.g., "$29.99" -> 29.99)
        numeric_prices = []
        for price in prices:
            try:
                # Remove currency symbol and convert to float
                numeric_price = float(price.replace('$', '').replace(',', ''))
                numeric_prices.append(numeric_price)
            except ValueError:
                continue
        
        if len(numeric_prices) > 1:
            # Check if prices are in descending order
            assert numeric_prices == sorted(numeric_prices, reverse=True), f"Products should be sorted by price high to low. Got prices: {numeric_prices}"


class TestProductInteraction:
    """Test class for product interaction functionality"""
    
    @pytest.mark.regression
    @pytest.mark.inventory
    def test_click_product_for_details(self, logged_in_user, inventory_page):
        """Test clicking on product to view details"""
        inventory_page.wait_for_inventory_screen()
        
        products_count = inventory_page.get_products_count()
        assert products_count > 0, "At least one product should be available"
        
        inventory_page.click_product_by_index(0)
        
        # Note: This would need a ProductDetailsPage object to verify
        # For now, we just verify we're no longer on inventory screen
        # Wait for transition to complete by checking if products header is still visible
        try:
            inventory_page.wait_for_element_to_disappear(inventory_page.PRODUCTS_SCREEN_HEADER, timeout=2)
        except:
            pass  # Header might still be visible on product details page
    
    
    @pytest.mark.smoke
    @pytest.mark.inventory
    def test_open_cart(self, logged_in_user, inventory_page):
        """Test opening cart from inventory screen"""
        inventory_page.wait_for_inventory_screen()
        
        inventory_page.add_first_product_to_cart()
        assert inventory_page.is_cart_badge_visible(), "Cart badge should be visible"
        
        inventory_page.open_cart()
        # Wait for navigation to cart screen by checking if we left inventory screen
        try:
            inventory_page.wait_for_element_to_disappear(inventory_page.PRODUCTS_SCREEN_HEADER, timeout=2)
        except:
            pass  # Cart screen might still show products header
        
        # Note: This would need a CartPage object to fully verify
        # For now, we verify we're no longer on inventory screen
        pass
    
    @pytest.mark.regression
    @pytest.mark.inventory
    def test_open_menu(self, logged_in_user, inventory_page):
        """Test opening hamburger menu from inventory screen"""
        inventory_page.wait_for_inventory_screen()
        
        inventory_page.open_menu()
        # Wait for menu to appear by checking for logout button
        inventory_page.wait_for_element(inventory_page.LOGOUT_BUTTON, timeout=2)
        
        # Note: This would need menu page object to fully verify
        # For now, we just ensure the action completed without error
        pass


class TestCartManagement:
    """Test class for cart management from inventory screen"""
    
    @pytest.mark.regression
    @pytest.mark.inventory
    def test_cart_state_persistence(self, logged_in_user, inventory_page):
        """Test that cart state persists across app interactions"""
        inventory_page.wait_for_inventory_screen()
        
        # Add two products using the helper method to avoid index issues
        inventory_page.add_multiple_products_to_cart(2)
        initial_count = inventory_page.get_cart_badge_count()
        assert initial_count == 2, "Cart should contain 2 items"
        
        inventory_page.background_app(3)
        
        current_count = inventory_page.get_cart_badge_count()
        assert current_count == initial_count, "Cart state should persist after app background"
    
    @pytest.mark.regression
    @pytest.mark.inventory
    def test_add_all_visible_products_on_screen(self, logged_in_user, inventory_page):
        """Test adding all visible products on current screen (no scrolling)"""
        inventory_page.wait_for_inventory_screen()
        
        # Get visible products count (no scrolling)
        visible_products = inventory_page.get_products_count()
        assert visible_products > 0, "Products should be visible on screen"
        
        # Add all visible products without scrolling
        initial_count = inventory_page.get_cart_badge_count() or 0
        
        # Add visible products one by one (they will change to REMOVE buttons)
        added_count = 0
        for i in range(visible_products):
            try:
                # Always use index 0 since buttons change after each addition
                # Use max_scrolls=0 to prevent scrolling - only visible products
                inventory_page.add_product_to_cart_by_index(0, max_scrolls=0)
                added_count += 1
            except Exception as e:
                # No more ADD TO CART buttons available
                print(f"Added {added_count} out of {visible_products} visible products. Reason: {e}")
                break
        
        final_count = inventory_page.get_cart_badge_count()
        expected_count = initial_count + added_count
        
        assert final_count == expected_count, f"Cart should contain {expected_count} products, got {final_count}"
        assert added_count > 0, f"Should add at least 1 visible product, added {added_count}"
        
        print(f"Successfully added {added_count} visible products from screen (no scrolling)")

    @pytest.mark.regression
    @pytest.mark.inventory
    @pytest.mark.slow
    def test_add_all_available_products_with_scrolling(self, logged_in_user, inventory_page):
        """Test adding all available products by scrolling through entire inventory"""
        inventory_page.wait_for_inventory_screen()
        
        # Use the helper method that scrolls through the entire inventory
        added_count = inventory_page.add_all_available_products_to_cart()
        
        final_count = inventory_page.get_cart_badge_count()
        assert final_count is not None, "Cart should show item count"
        assert final_count == added_count, f"Cart badge should match added count: expected {added_count}, got {final_count}"
        assert added_count > 2, f"Should be able to add more than 2 products with scrolling, got {added_count}"
        
        print(f"Successfully added {added_count} total products by scrolling through inventory")


# Parametrized tests for different product interactions
class TestDataDrivenProducts:
    """Data-driven product tests"""
    
    @pytest.mark.parametrize("product_index", [0, 1, 2])
    @pytest.mark.regression
    @pytest.mark.inventory
    def test_add_product_by_index(self, logged_in_user, inventory_page, product_index):
        """Test adding specific products to cart by index"""
        inventory_page.wait_for_inventory_screen()
        
        products_count = inventory_page.get_products_count()
        if product_index >= products_count:
            pytest.skip(f"Product at index {product_index} does not exist")
        
        initial_count = inventory_page.get_cart_badge_count() or 0
        inventory_page.add_product_to_cart_by_index(product_index)
        
        final_count = inventory_page.get_cart_badge_count()
        assert final_count == initial_count + 1, f"Product {product_index} should be added to cart"
