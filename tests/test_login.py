"""
Login functionality tests for SwagLabs Mobile App.
"""

import pytest
from page_objects.login_page import LoginPage
from page_objects.inventory_page import InventoryPage
from tests.base_test import BaseTest


class TestLogin (BaseTest):
    """Test class for login functionality"""

    @pytest.fixture(autouse=True)
    def setup_teardown(self, login_page, inventory_page):
        """Setup and teardown for each test"""
        # Setup: Before each test
        try:
            super().before_each(login_page, inventory_page)
        except Exception as e:
            # If before_each fails, just ensure we're on login screen
            login_page.wait_for_login_screen()
            
        yield  # This is where the test runs
        
        # Teardown: After each test
        try:
            super().after_each(login_page, inventory_page)
        except Exception as e:
            # If logout fails, that's okay for now - just log it
            print(f"Teardown warning: {e}")
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_with_standard_user(self, login_page, inventory_page, standard_user_credentials):
        """Test successful login with standard user"""
        login_page.wait_for_login_screen()
        assert login_page.is_displayed(), "Login screen should be displayed"
        
        login_page.login(
            standard_user_credentials["username"], 
            standard_user_credentials["password"]
        )
        
        inventory_page.wait_for_inventory_screen()
        assert inventory_page.is_displayed(), "User should be redirected to inventory screen"
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_with_locked_user(self, login_page, locked_user_credentials, test_data):
        """Test login attempt with locked out user"""
        login_page.wait_for_login_screen()
        
        login_page.login(
            locked_user_credentials["username"],
            locked_user_credentials["password"]
        )
        
        error_message = login_page.get_error_message()
        expected_error = test_data["error_messages"]["locked_out"]
        
        assert error_message is not None, "Error message should be displayed"
        assert expected_error in error_message, f"Expected '{expected_error}' in error message"
        
        assert login_page.is_displayed(), "User should remain on login screen"
    
    @pytest.mark.regression 
    @pytest.mark.login
    def test_login_with_invalid_credentials(self, login_page, invalid_user_credentials, test_data):
        """Test login attempt with invalid credentials"""
        login_page.wait_for_login_screen()
        
        login_page.login(
            invalid_user_credentials["username"],
            invalid_user_credentials["password"] 
        )
        
        error_message = login_page.get_error_message()
        expected_error = test_data["error_messages"]["invalid_credentials"]
        
        assert error_message is not None, "Error message should be displayed"
        assert expected_error in error_message, f"Expected '{expected_error}' in error message"
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_with_empty_username(self, login_page, test_data):
        """Test login attempt with empty username"""
        login_page.wait_for_login_screen()
        
        login_page.login("", "secret_sauce")
        
        error_message = login_page.get_error_message()
        expected_error = test_data["error_messages"]["username_required"]
        
        assert error_message is not None, "Error message should be displayed"
        assert expected_error in error_message, f"Expected '{expected_error}' in error message"
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_with_empty_password(self, login_page, test_data):
        """Test login attempt with empty password"""
        login_page.wait_for_login_screen()
        
        login_page.login("standard_user", "")
        
        error_message = login_page.get_error_message()
        expected_error = test_data["error_messages"]["password_required"]
        
        assert error_message is not None, "Error message should be displayed"
        assert expected_error in error_message, f"Expected '{expected_error}' in error message"
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_quick_login_standard_user(self, login_page, inventory_page):
        """Test quick login using standard user auto-fill button"""
        login_page.wait_for_login_screen()
        
        login_page.quick_login_standard_user()
        
        inventory_page.wait_for_inventory_screen()
        assert inventory_page.is_displayed(), "User should be redirected to inventory screen"
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_quick_login_locked_user(self, login_page, test_data):
        """Test quick login using locked user auto-fill button"""
        login_page.wait_for_login_screen()
        
        login_page.quick_login_locked_user()
        
        error_message = login_page.get_error_message()
        expected_error = test_data["error_messages"]["locked_out"]
        
        assert error_message is not None, "Error message should be displayed"
        assert expected_error in error_message, f"Expected '{expected_error}' in error message"


class TestLoginUI:
    """Test class for login UI elements and interactions"""
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_screen_elements(self, login_page):
        """Test that all login screen elements are present"""
        login_page.wait_for_login_screen()
        
        assert login_page.is_element_present(login_page.USERNAME_INPUT), "Username field should be present"
        
        assert login_page.is_element_present(login_page.PASSWORD_INPUT), "Password field should be present"
        
        assert login_page.is_element_present(login_page.LOGIN_BUTTON), "Login button should be present"

    @pytest.mark.regression
    @pytest.mark.login
    def test_field_interactions(self, login_page):
        """Test username and password field interactions"""
        login_page.wait_for_login_screen()
        
        login_page.enter_username("test_user")
        username_value = login_page.get_username_field_value()
        assert "test_user" in username_value, "Username should be entered correctly"
        
        login_page.enter_password("test_password")
        # Note: Password fields might not show text for security reasons
        
        login_page.clear_credentials()
        # Note: Verification depends on app behavior


class TestLoginFlow:
    """Test class for complete login flows and edge cases"""
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_multiple_failed_login_attempts(self, login_page):
        """Test multiple failed login attempts"""
        login_page.wait_for_login_screen()
        
        # Attempt multiple failed logins
        for attempt in range(3):
            login_page.login("invalid_user", "invalid_pass")
            
            error_message = login_page.get_error_message()
            assert error_message is not None, f"Error should be shown on attempt {attempt + 1}"
            
            # Clear error before next attempt
            login_page.clear_error_message()


# Parametrized tests for data-driven testing
class TestDataDrivenLogin:
    """Data-driven login tests"""
    
    @pytest.mark.parametrize("user_type,should_succeed", [
        ("standard_user", True),
        ("locked_out_user", False),
        ("problem_user", True),
        ("performance_glitch_user", True),
    ])
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_with_different_users(self, login_page, inventory_page, test_data, user_type, should_succeed):
        """Test login with different user types"""
        user = test_data["users"][user_type]
        
        login_page.wait_for_login_screen()
        login_page.login(user["username"], user["password"])
        
        if should_succeed:
            inventory_page.wait_for_inventory_screen()
            assert inventory_page.is_displayed(), f"{user_type} should login successfully"
        else:
            error_message = login_page.get_error_message()
            assert error_message is not None, f"{user_type} should show error message"
            assert login_page.is_displayed(), f"{user_type} should remain on login screen"
