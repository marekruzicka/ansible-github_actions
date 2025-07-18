## Relevant Files

- `github_actions.py` - Main Ansible callback plugin implementing GitHub Actions-compatible output, grouping, and summary statistics.
- `test_github_actions.py` - Unit tests for the callback plugin, covering output formatting, grouping, summary, and error handling.
- `README.md` - Documentation for plugin usage, configuration, and integration with GitHub Actions workflows.

### Notes

- Unit tests should be placed alongside the code files they are testing (e.g., `github_actions.py` and `test_github_actions.py` in the same directory).
- Use `pytest test_github_actions.py` to run tests. Running without a path executes all tests found by the pytest configuration.

## Tasks


- [ ] 1.0 Design the plugin architecture and configuration
- [x] 1.1 Review Ansible callback plugin API and requirements for 2.16+
  - Ansible callback plugins are Python modules placed in a callback_plugins directory or installed as packages. For 2.16+, plugins must define a class inheriting from `CallbackBase` in `ansible.plugins.callback`.
  - Required methods include `v2_playbook_on_start`, `v2_playbook_on_play_start`, `v2_playbook_on_task_start`, `v2_runner_on_ok`, `v2_runner_on_failed`, `v2_runner_on_skipped`, and `v2_playbook_on_stats`.
  - Plugins must set `CALLBACK_VERSION = 2.0` and `CALLBACK_TYPE = 'stdout'`.
  - Configuration is typically handled via environment variables or Ansible config files, accessible via `self.get_option()`.
  - Output should be written using `self._display.display()` for proper integration with Ansible's output system.
  - [ ] 1.2 Define configuration options (verbosity, archive filename)
  - [ ] 1.3 Plan data structures for tracking play/task results and summary statistics

- [ ] 2.0 Implement minimal, grouped output for GitHub Actions
  - [ ] 2.1 Implement output of filename, play name, hostname, status message, and task name per task
  - [ ] 2.2 Add grouping by play and task using `::group::` and `::endgroup::` markers
  - [ ] 2.3 Ensure output is concise and fits GitHub Actions UI constraints

- [ ] 3.0 Map Ansible status messages to GitHub Actions log levels
  - [ ] 3.1 Map 'ok' to 'notice', 'changed' to 'warning', 'failed' to 'error', and handle other statuses
  - [ ] 3.2 Test log level mapping for all supported status types

- [ ] 4.0 Implement summary statistics output (plain text)
  - [ ] 4.1 Track counts of ok, changed, failed, and skipped tasks, grouped by play and host
  - [ ] 4.2 Format and output summary statistics at the end of the run

- [ ] 5.0 Support writing all output to a plain text archive file
  - [ ] 5.1 Implement file writing logic for all output, including summary
  - [ ] 5.2 Make archive filename configurable
  - [ ] 5.3 Handle file I/O errors gracefully

- [ ] 6.0 Add configuration for verbosity and error handling
  - [ ] 6.1 Implement verbosity option to show detailed fail messages
  - [ ] 6.2 Ensure plugin does not crash on unexpected errors
  - [ ] 6.3 Add error handling for plugin logic and output formatting

- [ ] 7.0 Write unit tests for plugin functionality
  - [ ] 7.1 Test output formatting for all status types and grouping
  - [ ] 7.2 Test summary statistics output
  - [ ] 7.3 Test archive file writing and error handling
  - [ ] 7.4 Test configuration options (verbosity, filename)

- [ ] 8.0 Document plugin usage and configuration
  - [ ] 8.1 Write usage instructions for the plugin in `README.md`
  - [ ] 8.2 Document configuration options and integration steps for GitHub Actions
