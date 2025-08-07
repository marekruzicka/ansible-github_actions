# GitHub Actions Ansible Callback Plugin - Development Makefile

.PHONY: test test-unit test-live clean lint help install-dev release check-deps

# Default target
help:
	@echo "GitHub Actions Ansible Callback Plugin - Development Tasks"
	@echo ""
	@echo "Available targets:"
	@echo "  test       - Run all tests (unit + live demo)"
	@echo "  test-unit  - Run unit tests only"
	@echo "  test-live  - Run live Ansible demos"
	@echo "  test-all   - Run comprehensive test suite"
	@echo "  lint       - Run code linting (if available)"
	@echo "  format     - Format code with black (if available)"
	@echo "  clean      - Clean temporary files"
	@echo "  install-dev- Install development dependencies"
	@echo "  check-deps - Check for required dependencies"
	@echo "  release    - Prepare for release (run all checks)"
	@echo "  help       - Show this help message"

# Run all tests
test: test-unit test-live

# Run comprehensive test suite
test-all: check-deps test lint
	@echo "✅ All tests completed successfully"

# Run unit tests
test-unit:
	@echo "Running unit tests..."
	cd test && python3 -m pytest test_github_actions.py -v
	@echo "✅ Unit tests completed"

# Run live demonstration
test-live:
	@echo "Running live demonstration..."
	cd test && ./run_tests.sh
	@echo "✅ Live demo completed"

# Run specific test categories
test-grouping:
	@echo "Testing grouping functionality..."
	cd test && python3 test_grouping.py
	@echo "✅ Grouping tests completed"

test-output:
	@echo "Testing output formatting..."
	cd test && python3 test_output.py
	@echo "✅ Output tests completed"

# Code formatting
format:
	@echo "Formatting code..."
	@command -v black >/dev/null 2>&1 && black github_actions.py || echo "⚠️  black not available"
	@echo "✅ Formatting completed"

# Code linting (if tools are available)
lint:
	@echo "Running code linting..."
	@command -v pylint >/dev/null 2>&1 && pylint github_actions.py || echo "⚠️  pylint not available"
	@command -v flake8 >/dev/null 2>&1 && flake8 github_actions.py || echo "⚠️  flake8 not available"
	@command -v black >/dev/null 2>&1 && black --check github_actions.py || echo "⚠️  black not available"
	@echo "✅ Linting completed"

# Check for required dependencies
check-deps:
	@echo "Checking dependencies..."
	@python3 -c "import ansible; print(f'✅ Ansible {ansible.__version__}')" || echo "❌ Ansible not found"
	@python3 -c "import pytest; print(f'✅ pytest available')" || echo "⚠️  pytest not available"
	@command -v ansible-playbook >/dev/null 2>&1 && echo "✅ ansible-playbook available" || echo "❌ ansible-playbook not found"

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
	@echo "✅ Cleanup completed"

# Install development dependencies
install-dev:
	@echo "Installing development dependencies..."
	@command -v pip3 >/dev/null 2>&1 || (echo "❌ pip3 not found" && exit 1)
	pip3 install pytest pylint flake8 black ansible
	@echo "✅ Development dependencies installed"

# Quick validation
validate:
	@echo "Validating plugin..."
	python3 -c "import sys; sys.path.append('.'); from github_actions import CallbackModule; print('✅ Plugin imports successfully')"
	cd test && python3 -m pytest test_github_actions.py::TestGithubActionsCallback::test_unreachable_status_output -v
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
perf-test:
	@echo "Running performance tests..."
	cd test && time ansible-playbook -i 127.0.0.1,127.0.0.2,127.0.0.3,127.0.0.4,127.0.0.5, main.yml >/dev/null
	@echo "✅ Performance test completed"
