# 🚀 Getting Started - Quick Setup Guide

## ⚡ **5-Minute Setup**

### **1. Prerequisites Check**
```bash
# Verify you have these installed:
java -version        # Should show Java 17+
adb version         # Should show ADB version
node --version      # Should show Node.js 16+
appium --version    # Should show Appium 2.19.0+
```

### **2. Install Missing Components**
```bash
# Install Java (if missing)
brew install openjdk@17

# Install ADB (if missing)  
brew install android-platform-tools

# Install Appium & UiAutomator2 driver (if missing)
npm install -g appium
appium driver install uiautomator2
```

### **3. Environment Setup**
```bash
# Set environment variables (add to ~/.zshrc)
export ANDROID_HOME=~/Library/Android/sdk
export ANDROID_SDK_ROOT=$ANDROID_HOME
export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"

# Reload shell
source ~/.zshrc
```

### **4. Python Environment**
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 📱 **Emulator Setup**

### **Quick Emulator Creation**
1. **Open Android Studio**
2. **Tools** → **AVD Manager** → **Create Virtual Device**
3. **Select**: Pixel 6 Pro + API 33 (Android 13)
4. **Start** the emulator

### **Verify Emulator is Ready**
```bash
# Must show "device" status (not "offline")
adb devices

# Expected output:
# emulator-5554    device
```

---

## 🎯 **Run Your First Test**

### **Step-by-Step Test Execution**

```bash
# 1. Activate Python environment
source venv/bin/activate

# 2. Start Appium server
appium &

# 3. Verify Appium is running
curl -s http://localhost:4723/status

# 4. Check emulator is ready
adb devices

# 5. Run test
pytest tests/test_login.py::TestLogin::test_login_with_standard_user -v

# 6. ✅ Expected result: PASSED
```

---

## 📋 **Essential Commands**

### **Environment Management**
```bash
# Activate virtual environment
source venv/bin/activate

# Deactivate virtual environment
deactivate
```

### **Appium Server**
```bash
# Start Appium server
appium &

# Stop Appium server
pkill -f appium

# Check Appium status
curl http://localhost:4723/status
```

### **ADB Commands**
```bash
# List connected devices
adb devices

# Restart ADB (if device shows offline)
adb kill-server && adb start-server

# Connect to emulator
adb connect localhost:5555

# Check Android version
adb shell getprop ro.build.version.release
```

### **Test Execution**
```bash
# Run single test
pytest tests/test_login.py::TestLogin::test_login_with_standard_user -v

# Run all tests
pytest tests/ -v

# Run with HTML report
pytest tests/ --html=reports/report.html -v

# Run with auto-detect device
pytest tests/test_login.py --device=auto_detect -v
```

---

## 🔧 **Quick Troubleshooting**

| Issue | Solution |
|-------|----------|
| **"UiAutomator2 driver not found"** | `appium driver install uiautomator2` |
| **"ANDROID_HOME not set"** | `export ANDROID_HOME=~/Library/Android/sdk` |
| **"Java Runtime not found"** | `brew install openjdk@17` |
| **"Device offline"** | `adb kill-server && adb start-server` |
| **"Connection refused"** | `appium &` (start Appium server) |

---

## ✅ **Checklist Before Testing**

- [ ] **Java 17+** installed and in PATH
- [ ] **ADB** installed and working
- [ ] **Appium 2.19.0+** with UiAutomator2 driver
- [ ] **Android emulator** running (shows "device" in `adb devices`)
- [ ] **Virtual environment** activated
- [ ] **Appium server** running (responds to `curl http://localhost:4723/status`)

---

## 🎯 **Success Indicators**

When everything is working correctly:

```bash
$ adb devices
emulator-5554    device

$ curl -s http://localhost:4723/status | grep ready
"ready": true

$ pytest tests/test_login.py::TestLogin::test_login_with_standard_user -v
...
PASSED                                                           [100%]
```

---

## 📚 **Next Steps**

- **Explore Tests**: Check `tests/` directory for available test cases
- **Review Configuration**: See `config/capabilities.py` for device settings  
- **Page Objects**: Study `page_objects/` for automation patterns
- **Test Data**: Modify `data/test_users.json` for different test scenarios

**Ready to automate! 🚀** 