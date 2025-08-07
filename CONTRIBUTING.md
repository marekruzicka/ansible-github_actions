# Contributing to GitHub Actions Ansible Callback Plugin

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ansible-github-actions-callback
   ```

2. **Install development dependencies**
   ```bash
   make install-dev
   ```

3. **Validate the setup**
   ```bash
   make validate
   ```

## Testing

### Running Tests
```bash
# Run all tests
make test

# Run only unit tests
make test-unit

# Run only live demo
make test-live

# Test specific functionality
make test-grouping
make test-output
```

### Test Coverage
All contributions should maintain or improve test coverage:
- Unit tests in `test/test_github_actions.py`
- Functional tests using live Ansible execution
- Edge case testing for error conditions

## Code Standards

### Python Style
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings for all public methods
- Handle exceptions gracefully

### Testing Requirements
- All new features must include tests
- Bug fixes should include regression tests
- Tests must pass before submission

### Documentation
- Update README.md for new features
- Add entries to CHANGELOG.md
- Include usage examples where appropriate

## Submitting Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code following the standards above
   - Add/update tests as needed
   - Update documentation

3. **Test your changes**
   ```bash
   make test
   make lint  # if linting tools available
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Commit Message Format

Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test additions/changes
- `refactor:` for code refactoring
- `chore:` for maintenance tasks

Examples:
- `feat: add support for custom status icons`
- `fix: resolve smart grouping detection issue`
- `docs: update README with new configuration options`

## Bug Reports

When reporting bugs, please include:
- Ansible version
- Plugin configuration
- Steps to reproduce
- Expected vs actual behavior
- Relevant log output

## Feature Requests

For feature requests, please provide:
- Use case description
- Proposed implementation approach
- Examples of expected behavior
- Any relevant GitHub Actions workflow examples

## Code Review Process

All submissions go through code review:
1. Automated tests must pass
2. Code review by maintainers
3. Documentation review
4. Manual testing if needed

## Release Process

1. Update version in `__version__.py`
2. Update CHANGELOG.md
3. Create release tag
4. Update documentation if needed

Thank you for contributing!
