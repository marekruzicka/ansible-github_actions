# Changelog

All notable changes to the GitHub Actions Ansible Callback Plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Dynamic smart grouping that adapts during playbook execution
- Support for unreachable hosts with proper `::error::` formatting
- Comprehensive testing suite in `test/` directory
- Live demonstration playbook showcasing smart grouping
- Automated test script (`run_tests.sh`)
- Development Makefile for common tasks
- Enhanced documentation with examples and troubleshooting

### Changed
- Smart grouping now detects multiple hosts dynamically during execution
- Improved test organization - moved all tests to `test/` directory
- Updated README with comprehensive usage examples and configuration
- Enhanced ansible.cfg configuration with detailed comments

### Fixed
- Smart grouping now properly switches from play to task mode when multiple hosts detected
- Unreachable hosts now display with red error formatting in GitHub Actions
- Fixed test imports after reorganization
- Resolved duplicate configuration options in ansible.cfg

### Technical Details
- Added dynamic host tracking with `_seen_hosts` set
- Implemented mid-execution grouping strategy switching
- Enhanced `_emit_task_line` with smart grouping detection logic
- Added `unreachable` status case to formatting logic

## [Previous Versions]

### Features Implemented
- GitHub Actions workflow command support (`::group::`, `::notice::`, `::warning::`, `::error::`)
- Configurable grouping modes (smart, play, task)
- Statistics tracking per play and host
- Archive file support for output persistence
- Environment variable and ansible.cfg configuration
- Comprehensive error handling
- Changed task detection with proper status mapping
- Verbose mode for debugging

### Status Mapping
- `ok` → `::notice::` (blue info in GitHub Actions)
- `changed` → `::warning::` (yellow warning in GitHub Actions)
- `failed` → `::error::` (red error in GitHub Actions)
- `unreachable` → `::error::` (red error in GitHub Actions)
- `skipped` → plain text (no special formatting)

### Grouping Behavior
- **Smart Mode**: 
  - Single host: Groups by play for logical flow
  - Multiple hosts: Groups by task for parallel visibility
- **Play Mode**: Always groups by play regardless of host count
- **Task Mode**: Always groups by task regardless of host count
