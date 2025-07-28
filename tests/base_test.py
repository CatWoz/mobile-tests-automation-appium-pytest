"""
Base test class for SwagLabs Mobile App.
"""

import pytest
import subprocess
import logging
import time
from appium.webdriver.common.appiumby import AppiumBy

# Configure logging to see which method is used
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BaseTest:
    """Base test class with robust state management"""

    def before_each(self, login_page, inventory_page):
        """Before each test - ensure clean app state"""
        driver = login_page.driver
        start_time = time.time()
        
        logger.info("🔄 Starting app reset process...")
        
        # Try fastest methods first based on typical success rates
        reset_methods = [
            ("ADB Clear Data", self._clear_app_data_fast),
            ("App Restart", self._restart_app),
            ("Appium Reset", self._appium_reset),
            ("UI Logout", self._ui_logout_fallback)
        ]
        
        for method_name, method_func in reset_methods:
            try:
                method_start = time.time()
                logger.info(f"⏳ Trying {method_name}...")
                
                if method_func(driver, login_page, inventory_page):
                    method_duration = time.time() - method_start
                    total_duration = time.time() - start_time
                    logger.info(f"✅ {method_name} SUCCESS - {method_duration:.2f}s (total: {total_duration:.2f}s)")
                    
                    # Verify we're on login screen
                    login_page.wait_for_login_screen()
                    if login_page.is_displayed():
                        logger.info("✅ Login screen confirmed - reset complete!")
                        return
                    else:
                        logger.warning(f"⚠️ {method_name} succeeded but not on login screen")
                        continue
                        
            except Exception as e:
                method_duration = time.time() - method_start
                logger.warning(f"❌ {method_name} FAILED in {method_duration:.2f}s: {str(e)[:100]}")
                continue
        
        # If all methods failed, just ensure we wait for login screen
        logger.error("🚨 All reset methods failed - falling back to basic wait")
        login_page.wait_for_login_screen()

    def after_each(self, login_page, inventory_page):
        """After each test - optional cleanup"""
        pass
        
    def _clear_app_data_fast(self, driver, login_page, inventory_page):
        """Fast ADB clear data method (usually fastest for Android)"""
        if not hasattr(driver, 'capabilities') or driver.capabilities.get('platformName', '').lower() != 'android':
            raise Exception("Not Android platform")
            
        app_package = driver.capabilities.get('appium:appPackage', 'com.swaglabsmobileapp')
        
        # Get device ID quickly
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
        devices = [line.split('\t')[0] for line in result.stdout.strip().split('\n')[1:] if '\tdevice' in line]
        
        if not devices:
            raise Exception("No ADB devices found")
            
        device_id = devices[0]
        
        # Clear app data (fastest method)
        cmd = ['adb', '-s', device_id, 'shell', 'pm', 'clear', app_package]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
        
        if result.returncode != 0:
            raise Exception(f"ADB clear failed: {result.stderr}")
            
        # Force restart the app after clearing data
        time.sleep(0.5)  # Brief pause for data clear to complete
        driver.activate_app(app_package)
        
        return True
    
    def _restart_app(self, driver, login_page, inventory_page):
        """Restart the application (medium speed)"""
        app_package = driver.capabilities.get('appium:appPackage', 'com.swaglabsmobileapp')
        
        # Terminate and relaunch app
        driver.terminate_app(app_package)
        time.sleep(0.3)  # Brief pause between terminate and activate
        driver.activate_app(app_package)
        
        return True
    
    def _appium_reset(self, driver, login_page, inventory_page):
        """Use Appium's built-in reset (can be slow)"""
        driver.reset()
        return True
    
    def _ui_logout_fallback(self, driver, login_page, inventory_page):
        """UI logout fallback (slowest but most compatible)"""
        if not login_page.is_displayed() and inventory_page.is_displayed():
            logger.info("🔄 User appears to be logged in - attempting UI logout")
            inventory_page.logout()
            return True
        else:
            # Try navigation methods
            return self._force_app_to_login_screen(driver, login_page)

    def _force_app_to_login_screen(self, driver, login_page):
        """Force app to login screen using various methods"""
        # Method 1: Try back button presses to get to login
        for i in range(3):
            try:
                driver.back()
                time.sleep(0.2)
                if login_page.is_displayed():
                    return True
            except Exception:
                continue
                
        # Method 2: Try home button + relaunch
        try:
            driver.background_app(1)  # Background for 1 second
            app_package = driver.capabilities.get('appium:appPackage', 'com.swaglabsmobileapp')
            driver.activate_app(app_package)
            return True
        except Exception:
            pass
            
        return False
