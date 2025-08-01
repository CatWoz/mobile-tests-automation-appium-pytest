# Mobile Test Automation Makefile

.PHONY: help install setup setup-reports download-apps clean clean-reports test test-android test-ios reports

# Default target
help: ## Show this help message
	@echo "📱 Mobile Test Automation - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Setup and Installation
install: ## Install Python dependencies
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt

setup: install setup-reports ## Complete project setup
	@echo "🔧 Setting up project..."
	mkdir -p apps/android apps/ios
	@echo "✅ Project setup completed!"

download-apps: ## Download application files
	@echo "📱 Downloading mobile applications..."
	python scripts/download_apps.py --platform all

# Testing Commands
test: ## Run all tests (default platform: android)
	@echo "🧪 Running all mobile tests..."
	pytest tests/ --platform=android -v

test-android: ## Run Android tests
	@echo "🤖 Running Android tests..."
	pytest tests/ --platform=android -v

test-ios: ## Run iOS tests  
	@echo "🍎 Running iOS tests..."
	pytest tests/ --platform=ios -v

test-smoke: ## Run smoke tests only
	@echo "💨 Running smoke tests..."
	pytest tests/ -m smoke -v

test-regression: ## Run regression tests only
	@echo "🔄 Running regression tests..."
	pytest tests/ -m regression -v

test-login: ## Run login tests only
	@echo "🔑 Running login tests..."
	pytest tests/ -m login -v

test-inventory: ## Run inventory tests only
	@echo "📦 Running inventory tests..."
	pytest tests/ -m inventory -v

test-parallel: ## Run tests in parallel
	@echo "⚡ Running tests in parallel..."
	pytest tests/ -n auto --platform=android -v

# Reports Commands
reports: ## Generate and view test reports
	@echo "📊 Opening test reports..."
	@echo "HTML Report: reports/pytest-report.html"
	@echo "JSON Report: reports/report.json"
	@open reports/pytest-report.html 2>/dev/null || echo "Open reports/pytest-report.html manually"

setup-reports: ## Create reports directories
	@echo "📁 Creating reports directories..."
	mkdir -p reports/screenshots
	@echo "✅ Reports directories created!"

clean-reports: ## Clean generated reports
	@echo "🗑️ Cleaning reports..."
	rm -rf reports/pytest-report.html reports/report.json
	@echo "✅ Reports cleaned!"

# Maintenance Commands  
clean: clean-reports ## Clean temporary files and reports
	@echo "🧹 Cleaning temporary files..."
	rm -rf .pytest_cache __pycache__ */__pycache__ */*/__pycache__
	find . -name "*.pyc" -delete
	@echo "✅ Cleanup completed!"

clean-apps: ## Remove downloaded apps
	@echo "🗑️ Removing downloaded apps..."
	rm -rf apps/android/* apps/ios/*

lint: ## Run code linting
	@echo "🔍 Running code linting..."
	flake8 page_objects/ tests/ config/ --max-line-length=120
	black --check page_objects/ tests/ config/

format: ## Format code with Black
	@echo "✨ Formatting code..."
	black page_objects/ tests/ config/

# Appium Commands
appium-start: ## Start local Appium server
	@echo "🚀 Starting Appium server..."
	appium --port 4723 --relaxed-security &

appium-stop: ## Stop local Appium server
	@echo "🛑 Stopping Appium server..."
	pkill -f appium || echo "Appium server not running"

appium-doctor: ## Run Appium Doctor
	@echo "🩺 Running Appium Doctor..."
	appium-doctor

# Device Commands
devices: ## List connected devices
	@echo "📱 Connected devices:"
	adb devices

android-install: ## Install Android APK on connected device
	@echo "📲 Installing Android app..."
	adb install -r apps/android/Android.SauceLabs.Mobile.Sample.app.2.7.1.apk

# Environment Commands
check-env: ## Check environment setup
	@echo "🔍 Checking environment setup..."
	@echo "Python version:"
	python --version
	@echo "Pip packages:"
	pip list | grep -E "(appium|selenium|pytest)"
	@echo "Java version:"
	java -version || echo "Java not found"
	@echo "Node.js version:"
	node --version || echo "Node.js not found"
	@echo "Appium version:"
	appium --version || echo "Appium not found"

install-appium: ## Install Appium globally
	@echo "📲 Installing Appium..."
	npm install -g appium
	npm install -g @appium/doctor

# Quick Start Commands
quick-start: setup download-apps ## Complete quick start setup
	@echo "🚀 Quick start completed!"
	@echo "Next steps:"
	@echo "1. Start Appium server: make appium-start"
	@echo "2. Run tests: make test"
	@echo "3. View reports: make reports"

demo: ## Run a quick demo test
	@echo "🎬 Running demo test..."
	pytest tests/test_login.py::TestLogin::test_login_with_standard_user --platform=android -v

# Info Commands
info: ## Show project information
	@echo "📱 Mobile Test Automation Project"
	@echo "=================================="
	@echo "Framework: Appium + pytest + Page Object Model"
	@echo "Languages: Python 3.9+"
	@echo "Platforms: Android, iOS"
	@echo ""
	@echo "📁 Project Structure:"
	@echo "├── 📱 apps/           - APK/IPA files"
	@echo "├── 🧪 tests/          - Test files" 
	@echo "├── 📄 page_objects/   - Page Object Model"
	@echo "├── ⚙️ config/         - Configuration"
	@echo "├── 📊 data/           - Test data"

status: ## Show current status
	@echo "📊 Current Status:"
	@echo "=================="
	@echo "Apps downloaded:"
	@ls -la apps/android/ apps/ios/ 2>/dev/null | grep -E "\.(apk|app|ipa)$$" | wc -l | xargs echo
	@echo "Docker status:"
	@docker-compose ps 2>/dev/null || echo "Docker not running" 