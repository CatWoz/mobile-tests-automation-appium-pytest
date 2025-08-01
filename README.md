# 📱 Mobile Test Automation Framework

A comprehensive Appium-based mobile test automation framework for Android and iOS applications, built with Python and pytest.

## 🚀 **Quick Start**

This framework runs **locally** with Appium server and Android emulators for reliable mobile testing.

---

## 📋 **Prerequisites**

### **1. System Requirements**
- **macOS**: 10.15+ (or Linux/Windows)
- **Python**: 3.8+
- **Node.js**: 16+
- **Java**: 17+ (Required for APK signature verification)
- **Android Studio**: For emulator management

### **2. Core Dependencies**
- **Appium**: 2.19.0+ 
- **UiAutomator2 Driver**: For Android automation
- **ADB**: Android Debug Bridge
- **Virtual Environment**: For Python dependencies

---

## 🛠️ **Installation Guide**

### **Step 1: Install Java**
```bash
# Install Java 17 via Homebrew (macOS)
brew install openjdk@17

# Add to PATH
export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"

# Verify installation
java -version
```

### **Step 2: Install Android Studio & ADB**
```bash
# Install ADB via Homebrew
brew install android-platform-tools

# Verify ADB installation
adb version

# Download Android Studio from: https://developer.android.com/studio
# Install and set up Android SDK
```

### **Step 3: Install Appium & UiAutomator2 Driver**
```bash
# Install Appium globally
npm install -g appium

# Install UiAutomator2 driver for Android
appium driver install uiautomator2

# Verify installation
appium driver list --installed
```

### **Step 4: Set Environment Variables Globally**

**Method 1: Automatic Setup (Recommended)**
```bash
# Add environment variables to your shell profile
echo 'export ANDROID_HOME=~/Library/Android/sdk' >> ~/.zshrc
echo 'export ANDROID_SDK_ROOT=$ANDROID_HOME' >> ~/.zshrc
echo 'export PATH=$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/tools:$ANDROID_HOME/build-tools' >> ~/.zshrc
echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc

# For bash users (if using bash instead of zsh)
echo 'export ANDROID_HOME=~/Library/Android/sdk' >> ~/.bash_profile
echo 'export ANDROID_SDK_ROOT=$ANDROID_HOME' >> ~/.bash_profile
echo 'export PATH=$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/tools:$ANDROID_HOME/build-tools' >> ~/.bash_profile
echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.bash_profile

# Reload your shell configuration
source ~/.zshrc  # or source ~/.bash_profile for bash users
```

**Method 2: Manual Setup**
```bash
# Open your shell configuration file
nano ~/.zshrc  # or ~/.bash_profile for bash

# Add these lines at the end of the file:
export ANDROID_HOME=~/Library/Android/sdk
export ANDROID_SDK_ROOT=$ANDROID_HOME
export PATH=$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/tools:$ANDROID_HOME/build-tools
export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"

# Save and exit (Ctrl+X, Y, Enter in nano)
# Reload configuration
source ~/.zshrc
```

**Verify Environment Variables**
```bash
# Check if variables are set correctly
echo $ANDROID_HOME          # Should show: /Users/yourname/Library/Android/sdk
echo $ANDROID_SDK_ROOT       # Should show: /Users/yourname/Library/Android/sdk
echo $PATH | grep android    # Should show Android SDK paths
java -version               # Should show Java 17.x.x
adb version                # Should show ADB version
```

**Path Details Explained:**
- **ANDROID_HOME**: Main Android SDK directory
- **ANDROID_SDK_ROOT**: Alternative SDK variable (some tools require this)
- **platform-tools**: Contains ADB, fastboot
- **tools**: Contains Android SDK tools
- **build-tools**: Contains apksigner, zipalign for APK operations
- **Java PATH**: Required for APK signature verification

### **Step 5: Create Python Virtual Environment**
```bash
# Navigate to project directory
cd mobile-test-automation

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

---

## 📱 **Android Emulator Setup**

### **Create Android Emulator**
1. **Open Android Studio**
2. **Tools** → **AVD Manager**
3. **Create Virtual Device**
4. **Choose Device**: Pixel 6 Pro
5. **Select System Image**: API 33 (Android 13) or API 34 (Android 14)
6. **Finish** and **Start** the emulator

### **Verify Emulator is Ready**
```bash
# Check running emulators
adb devices

# Should show:
# emulator-5554    device

# Check Android version
adb shell getprop ro.build.version.release

# Check device properties
adb shell getprop ro.product.model
```

### **Emulator Troubleshooting**
```bash
# Restart ADB if device shows "offline"
adb kill-server && adb start-server

# Reconnect to emulator
adb connect localhost:5555

# Check emulator status
adb devices -l
```

---

## 🎯 **Running Tests**

### **1. Start Appium Server**
```bash
# Set environment variables and start Appium
export ANDROID_HOME=~/Library/Android/sdk
export ANDROID_SDK_ROOT=$ANDROID_HOME
export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"

# Start Appium server in background
appium &

# Verify server is running
curl -s http://localhost:4723/status | python3 -m json.tool
```

### **2. Verify Setup is Ready**
```bash
# Check all components
adb devices                    # Should show "device" status
appium driver list --installed # Should show uiautomator2
java -version                  # Should show Java 17+
```

### **3. Run Tests**
```bash
# Activate virtual environment
source venv/bin/activate

# Run single test
pytest tests/test_login.py::TestLogin::test_login_with_standard_user -v

# Run all login tests
pytest tests/test_login.py -v

# Run all tests
pytest tests/ -v

# Run with specific device configuration
pytest tests/test_login.py --device=auto_detect -v

# Run with detailed output
pytest tests/test_login.py -v -s
```

### **4. Generate Reports**
```bash
# Run tests with HTML report
pytest tests/ --html=reports/report.html -v

# Run tests with Allure reports
pytest tests/ --alluredir=reports/allure-results -v

# Generate Allure report
allure serve reports/allure-results
```

---

## 🧪 **Advanced Test Running Options**

### **Cart Tests**
```bash
# All cart tests
pytest tests/test_cart.py -v

# Smoke cart tests only  
pytest tests/test_cart.py -m smoke -v

# Cart tests by functionality
pytest tests/test_cart.py::TestCartFunctionality -v
pytest tests/test_cart.py::TestRemoveFromCartPage -v

# Specific cart test
pytest tests/test_cart.py::TestCartFunctionality::test_add_product_and_verify_in_cart -v
```

### **E2E Purchase Tests**
```bash
# All E2E purchase tests
pytest tests/test_e2e_purchase.py -v

# Smoke E2E tests only
pytest tests/test_e2e_purchase.py -m smoke -v

# Full E2E purchase flow
pytest tests/test_e2e_purchase.py::TestE2EPurchaseFlow::test_complete_purchase_flow_single_product -v
```

### **Combined Test Runs**
```bash
# All cart and E2E tests
pytest tests/test_cart.py tests/test_e2e_purchase.py -v

# All smoke tests (across all modules)
pytest -m "smoke" -v

# All purchase-related tests
pytest -m "cart or purchase" -v

# All E2E tests (cart + purchase)
pytest -m "e2e" -v

# All regression tests
pytest -m "regression" -v
```

### **Test Filtering by Markers**
```bash
# Available markers:
# - smoke: Critical functionality tests
# - regression: Comprehensive functionality tests  
# - cart: Shopping cart tests
# - e2e: End-to-end test scenarios
# - purchase: Purchase flow tests
# - login: Login functionality tests
# - inventory: Product inventory tests
# - slow: Tests that take longer to run

# Run specific marker combinations
pytest -m "smoke and cart" -v          # Smoke cart tests
pytest -m "regression and not slow" -v  # Fast regression tests
pytest -m "e2e or smoke" -v            # All critical and E2E tests
```

### **Advanced Execution Options**
```bash
# With custom timeout
pytest tests/test_cart.py -v --timeout=300

# Parallel execution (if xdist installed)
pytest tests/ -v -n auto

# Stop on first failure
pytest tests/ -v -x

# Run last failed tests
pytest tests/ -v --lf

# Run tests and show coverage
pytest tests/ -v --cov=page_objects --cov-report=html

# Detailed output with step-by-step info
pytest tests/test_cart.py -v -s --tb=long

# Silent mode (minimal output)
pytest tests/test_cart.py -q
```

### **Output and Reporting Options**
```bash
# JSON report with custom file name
pytest tests/test_cart.py -v --json-report --json-report-file=reports/cart-report.json

# HTML report with custom styling
pytest tests/test_cart.py -v --html=reports/cart-report.html --self-contained-html

# JUnit XML format (for CI/CD)
pytest tests/ -v --junitxml=reports/junit.xml

# Multiple output formats
pytest tests/test_cart.py -v \
  --html=reports/cart.html \
  --json-report --json-report-file=reports/cart.json \
  --junitxml=reports/cart-junit.xml
```

### **Development and Debugging**
```bash
# Run with Python debugger on failures
pytest tests/test_cart.py -v --pdb

# Capture and show all output
pytest tests/test_cart.py -v -s --capture=no

# Run specific test with maximum verbosity
pytest tests/test_cart.py::TestCartFunctionality::test_add_product_and_verify_in_cart -vvv -s

# Show local variables on failures
pytest tests/test_cart.py -v -l

# Show durations of slowest tests
pytest tests/ -v --durations=10
```

### **Quick Test Commands**
```bash
# Quick smoke test across all modules
pytest -m smoke -v --tb=short

# Quick cart functionality check
pytest tests/test_cart.py::TestCartFunctionality -v -q

# Run main E2E flow (most important test)
pytest tests/test_e2e_purchase.py::TestE2EPurchaseFlow::test_complete_purchase_flow_single_product -v -s
```

---

## 📊 **Test Configuration**

### **Available Device Configurations**
- `pixel_3_api_29`: Android 10.0
- `pixel_6_api_33`: Android 13.0  
- `samsung_galaxy_s21`: Android 11.0
- `auto_detect`: Auto-detect available device

### **Configuration Files**
- `config/capabilities.py`: Device capabilities and Appium settings
- `pytest.ini`: Pytest configuration and markers
- `requirements.txt`: Python dependencies

---

## 🔧 **Troubleshooting**

### **Common Issues**

**1. "Could not find a driver for automationName 'UiAutomator2'"**
```bash
# Install UiAutomator2 driver
appium driver install uiautomator2
```

**2. "Neither ANDROID_HOME nor ANDROID_SDK_ROOT environment variable was exported"**
```bash
# Set environment variables
export ANDROID_HOME=~/Library/Android/sdk
export ANDROID_SDK_ROOT=$ANDROID_HOME
```

**3. "Unable to locate a Java Runtime"**
```bash
# Install Java 17
brew install openjdk@17
export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"
```

**4. "Device offline" in ADB**
```bash
# Restart ADB and reconnect
adb kill-server && adb start-server
adb connect localhost:5555
```

**5. Test fails with connection errors**
```bash
# Check Appium server is running
curl http://localhost:4723/status

# Restart Appium if needed
pkill -f appium && appium &
```

---

## 📁 **Project Structure**

```
mobile-test-automation/
├── config/
│   ├── capabilities.py      # Device configurations
│   └── __init__.py
├── page_objects/
│   ├── base_page.py          # Base page object class
│   ├── login_page.py         # Login page object
│   ├── inventory_page.py     # Inventory page object
│   ├── cart_page.py          # Shopping cart page object
│   ├── checkout_page.py      # Checkout form page object
│   ├── order_overview_page.py # Order overview page object
│   ├── confirmation_page.py  # Order confirmation page object
│   └── __init__.py
├── tests/
│   ├── conftest.py           # Pytest configuration
│   ├── base_test.py          # Base test class
│   ├── test_login.py         # Login test cases
│   ├── test_inventory.py     # Inventory test cases
│   ├── test_cart.py          # Shopping cart test cases
│   ├── test_e2e_purchase.py  # End-to-end purchase tests
│   └── __init__.py
├── apps/
│   └── android/              # Android APK files
├── data/
│   └── test_users.json       # Test data
├── reports/                  # Test reports
├── requirements.txt          # Python dependencies
├── pytest.ini              # Pytest settings
├── README_CART_AND_E2E.md   # Cart and E2E testing guide
└── E2E_TESTS_FIXES_SUMMARY.md # E2E tests fixes and status summary
```

---

## 🎯 **Example Test Command Flow**

```bash
# 1. Start emulator (Android Studio)
# 2. Verify emulator is ready
adb devices

# 3. Activate Python environment
source venv/bin/activate

# 4. Start Appium server
appium &

# 5. Run tests
pytest tests/test_login.py::TestLogin::test_login_with_standard_user -v

# 6. View results
# ✅ PASSED - Test completed successfully
```

---

## 🤝 **Contributing**

1. Ensure all tests pass locally
2. Follow the existing code structure
3. Add tests for new features
4. Update documentation as needed

---

## 📧 **Support**

For issues or questions:
- Check the troubleshooting section above
- Verify all prerequisites are installed
- Ensure emulator is running with "device" status in ADB 