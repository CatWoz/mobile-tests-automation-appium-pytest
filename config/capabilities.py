"""
Appium capabilities configuration for different platforms and devices.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory for the project
BASE_DIR = Path(__file__).parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")

# App directories
ANDROID_APP_DIR = BASE_DIR / "apps/android"
IOS_APP_DIR = BASE_DIR / "apps/ios"

def get_android_app_path():
    """Get Android app path dynamically from environment variable or find APK file"""
    # Try to get filename from environment variable
    app_filename = os.getenv('ANDROID_APP_APK_FILENAME')
    
    if app_filename:
        app_path = ANDROID_APP_DIR / app_filename
        if app_path.exists():
            return str(app_path)
    
    # Fallback: find any APK file in the Android directory
    android_dir = Path(ANDROID_APP_DIR)
    apk_files = list(android_dir.glob("*.apk"))
    if apk_files:
        return str(apk_files[0])
    
    # Final fallback: return the default expected path
    return str(ANDROID_APP_DIR/app_filename)

def get_ios_app_path():
    """Get iOS app path dynamically from environment variable or find app file"""
    # Try to get filename from environment variable
    app_filename = os.getenv('IOS_APP_FILENAME_ZIP')
    
    if app_filename:
        # Check if it's a zip file, extract .app name
        if app_filename.endswith('.zip'):
            app_name = app_filename.replace('.zip', '')
            app_path = IOS_APP_DIR / app_name
            if app_path.exists():
                return str(app_path)
        
        # Direct file check
        app_path = IOS_APP_DIR / app_filename
        if app_path.exists():
            return str(app_path)
    
    # Fallback: find any iOS app file in the directory
    ios_dir = Path(IOS_APP_DIR)
    
    # First look for .ipa files (for real devices)
    ipa_files = list(ios_dir.glob("*.ipa"))
    if ipa_files:
        return str(ipa_files[0])
    
    # Then look for .app files (for simulators)
    app_files = list(ios_dir.glob("*.app"))
    if app_files:
        return str(app_files[0])
    
    # Also check for extracted .app from zip
    for item in ios_dir.iterdir():
        if item.is_dir() and item.name.endswith('.app'):
            return str(item)
    
    return None

# Common capabilities
COMMON_CAPS = {
    "platformVersion": "auto",
    "automationName": "auto",
    "noReset": False,  # Allow app state reset for clean tests
    "fullReset": False,  # Don't uninstall/reinstall every time
    "newCommandTimeout": 300,
    "launchTimeout": 90000,
    "deviceReadyTimeout": 90,
    "androidDeviceReadyTimeout": 90,
    "iosInstallPause": 8000,
    "androidInstallTimeout": 90000,
    "autoGrantPermissions": True,
    "autoAcceptAlerts": True,
    "autoDismissAlerts": True,
    # Reset settings for reliable test isolation
    "forceAppLaunch": True,
    "shouldTerminateApp": True,
}

# Android Configurations
# All Android configurations use UiAutomator2 automation driver
# Requirements: appium driver install uiautomator2
ANDROID_CAPS = {
    "pixel_3a_api_36": {
        **COMMON_CAPS,
        "platformName": "Android",
        "platformVersion": "16",
        "deviceName": "Pixel_3a_API_36",
        "automationName": "UiAutomator2",
        "app": get_android_app_path(),
        "appPackage": "com.swaglabsmobileapp",
        "appActivity": "com.swaglabsmobileapp.MainActivity",
        "ensureWebviewsHavePages": True,
        "nativeWebScreenshot": True,
        "connectHardwareKeyboard": True,
    },
    
    "auto_detect": {
        **COMMON_CAPS,
        "platformName": "Android",
        "platformVersion": "16",
        "automationName": "UiAutomator2",
        "app": get_android_app_path(),
        "appPackage": "com.swaglabsmobileapp",
        "appActivity": "com.swaglabsmobileapp.MainActivity",
    }
}

# iOS Configurations
IOS_CAPS = {
    "iphone_15_pro_ios_17.5": {
        **COMMON_CAPS,
        "platformName": "iOS",
        "platformVersion": "17.5",
        "deviceName": "iPhone 15 Pro",
        "automationName": "XCUITest",
        "app": get_ios_app_path(),
        "bundleId": "com.saucelabs.SwagLabsMobileApp",
        "shouldUseSingleton": False,
        "shouldUseTestManagerForVisibilityDetection": False,
    },
    
    "auto_detect": {
        **COMMON_CAPS,
        "platformName": "iOS",
        "automationName": "XCUITest",
        "app": get_ios_app_path(),
        "bundleId": "com.saucelabs.SwagLabsMobileApp",
        # deviceName and platformVersion will be auto-detected
        "xcodeOrgId": "YOUR_TEAM_ID",  # Required for real device
        "xcodeSigningId": "iPhone Developer",
        "updatedWDABundleId": "com.yourcompany.WebDriverAgentRunner",
    }
}

def get_capabilities(platform, device_config="default"):
    """
    Get capabilities for specified platform and device configuration.
    
    Args:
        platform (str): 'android' or 'ios'
        device_config (str): Device configuration name
    
    Returns:
        dict: Appium capabilities
    """
    # Local execution
    if platform == "android":
        if device_config == "default":
            device_config = "auto_detect"
        
        if device_config in ANDROID_CAPS:
            caps = ANDROID_CAPS[device_config].copy()
            
            # Verify app exists
            if not Path(caps["app"]).exists():
                raise FileNotFoundError(f"Android app not found: {caps['app']}")
            
            return caps
        else:
            raise ValueError(f"Unknown Android device config: {device_config}")
    
    elif platform == "ios":
        if device_config == "default":
            device_config = "auto_detect"
        
        if device_config in IOS_CAPS:
            caps = IOS_CAPS[device_config].copy()
            
            # Verify app exists
            if not caps["app"] or not Path(caps["app"]).exists():
                raise FileNotFoundError(f"iOS app not found: {caps['app']}")
            
            return caps
        else:
            raise ValueError(f"Unknown iOS device config: {device_config}")
    
    else:
        raise ValueError(f"Unknown platform: {platform}")

def list_available_configs():
    """List all available device configurations"""
    configs = {
        "android": list(ANDROID_CAPS.keys()),
        "ios": list(IOS_CAPS.keys())
    }
    return configs

# Appium server configuration
APPIUM_SERVER_CONFIG = {
    "local": {
        "server_url": "http://localhost:4723",
        "command_executor": "http://localhost:4723"
    }
}

def get_server_url():
    """Get Appium server URL for local execution"""
    return APPIUM_SERVER_CONFIG["local"]["server_url"] 