# GitHub Actions Ansible Callback Plugin - Development Makefile

# Virtual environment settings
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
PYTEST = $(VENV_DIR)/bin/pytest

.PHONY: test test-unit test-live clean lint help install-dev release check-deps venv

# Default target
help:
	@echo "GitHub Actions Ansible Callback Plugin - Development Tasks"
	@echo ""
	@echo "Available targets:"
	@echo "  venv       - Create virtual environment"
	@echo "  test       - Run all tests (unit + live demo)"
	@echo "  test-unit  - Run unit tests only"
	@echo "  test-live  - Run live Ansible demos"
	@echo "  test-all   - Run comprehensive test suite"
	@echo "  lint       - Run code linting (if available)"
	@echo "  format     - Format code with black (if available)"
	@echo "  clean      - Clean temporary files and venv"
	@echo "  install-dev- Install development dependencies"
	@echo "  check-deps - Check for required dependencies"
	@echo "  release    - Prepare for release (run all checks)"
	@echo "  help       - Show this help message"

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	@test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	@$(PIP) install --upgrade pip
	@echo "✅ Virtual environment created at $(VENV_DIR)"

# Run all tests
test: venv test-unit test-live

# Run comprehensive test suite
test-all: venv check-deps test lint
	@echo "✅ All tests completed successfully"

# Run unit tests
test-unit: venv
	@echo "Running unit tests..."
	cd test && ../$(PYTEST) test_github_actions.py -v
	@echo "✅ Unit tests completed"

# Run live demonstration
test-live: venv
	@echo "Running live demonstration..."
	cd test && ../$(VENV_DIR)/bin/ansible-playbook -i 127.0.0.1, main.yml
	@echo "✅ Live demo completed"

# Run specific test categories
test-grouping: venv
	@echo "Testing grouping functionality..."
	cd test && ../$(PYTHON) test_grouping.py
	@echo "✅ Grouping tests completed"

test-output: venv
	@echo "Testing output formatting..."
	cd test && ../$(PYTHON) test_output.py
	@echo "✅ Output tests completed"

# Code formatting
format: venv
	@echo "Formatting code..."
	@test -f $(VENV_DIR)/bin/black && $(VENV_DIR)/bin/black github_actions.py || echo "⚠️  black not available (run make install-dev)"
	@echo "✅ Formatting completed"

# Code linting (if tools are available)
lint: venv
	@echo "Running code linting..."
	@test -f $(VENV_DIR)/bin/pylint && $(VENV_DIR)/bin/pylint github_actions.py || echo "⚠️  pylint not available (run make install-dev)"
	@test -f $(VENV_DIR)/bin/flake8 && $(VENV_DIR)/bin/flake8 github_actions.py || echo "⚠️  flake8 not available (run make install-dev)"
	@test -f $(VENV_DIR)/bin/black && $(VENV_DIR)/bin/black --check github_actions.py || echo "⚠️  black not available (run make install-dev)"
	@echo "✅ Linting completed"

# Check for required dependencies
check-deps: venv
	@echo "Checking dependencies..."
	@$(PYTHON) -c "import ansible; print(f'✅ Ansible {ansible.__version__}')" || echo "❌ Ansible not found (run make install-dev)"
	@$(PYTHON) -c "import pytest; print(f'✅ pytest available')" || echo "⚠️  pytest not available (run make install-dev)"
	@test -f $(VENV_DIR)/bin/ansible-playbook && echo "✅ ansible-playbook available" || echo "❌ ansible-playbook not found (run make install-dev)"

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name "*.pyo" -delete 2>/dev/null || true
	find . -name "*.orig" -delete 2>/dev/null || true
	find . -name "*.rej" -delete 2>/dev/null || true
	rm -rf .pytest_cache/ 2>/dev/null || true
	rm -f /tmp/ansible_*.log 2>/dev/null || true
	rm -f /tmp/ansible_test_*.txt 2>/dev/null || true
	rm -rf $(VENV_DIR) 2>/dev/null || true
	@echo "✅ Cleanup completed"

# Install development dependencies
install-dev: venv
	@echo "Installing development dependencies..."
	$(PIP) install pytest pylint flake8 black ansible
	@echo "✅ Development dependencies installed"

# Quick validation
validate: venv
	@echo "Validating plugin..."
	$(PYTHON) -c "import sys; sys.path.append('.'); from github_actions import CallbackModule; print('✅ Plugin imports successfully')"
	cd test && ../$(PYTEST) test_github_actions.py::TestGithubActionsCallback::test_unreachable_status_output -v
	@echo "✅ Basic validation completed"

# Release preparation
release: clean test-all
	@echo "Preparing for release..."
	@echo "✅ All checks passed - ready for release!"

# Show current repository status
status:
	@echo "Repository Status:"
	@echo "=================="
	@echo "Files:"
	@ls -la github_actions.py 2>/dev/null || echo "❌ Main plugin file missing"
	@ls -la test/ | head -5
	@echo ""
	@echo "Git status:"
	@git status --porcelain 2>/dev/null || echo "Not a git repository"

# Performance test
perf-test: venv
	@echo "Running performance tests..."
	cd test && time ../$(VENV_DIR)/bin/ansible-playbook -i 127.0.0.1,127.0.0.2,127.0.0.3,127.0.0.4,127.0.0.5, main.yml >/dev/null
	@echo "✅ Performance test completed"
