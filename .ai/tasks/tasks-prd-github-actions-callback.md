## Relevant Files

- `github_actions.py` - Main callback plugin implementation for GitHub Actions output formatting.
- `test_github_actions.py` - Unit tests for the callback plugin.

### Notes

- Unit tests should be placed alongside the main plugin file.
- Use `python -m pytest test_github_actions.py -v` to run tests.
- The plugin must be compatible with Ansible 2.16+ callback API.

## Tasks

- [x] 1.0 Implement missing status handlers and fix group management
  - [x] 1.1 Add v2_runner_on_changed method to handle changed status
  - [x] 1.2 Fix group management to properly open/close play and task groups
  - [x] 1.3 Update _emit_task_line to handle 'changed' status mapping
- [x] 2.0 Add configuration support for verbosity and archive file output
  - [x] 2.1 Add callback plugin configuration options (verbose, archive_file)
  - [x] 2.2 Implement configuration parsing in __init__ method
  - [x] 2.3 Add verbose error message output for failed tasks
- [x] 3.0 Implement statistics tracking and summary output
  - [x] 3.1 Add statistics tracking data structures (counters by play/host)
  - [x] 3.2 Update task result handlers to increment counters
  - [x] 3.3 Implement summary output in v2_playbook_on_stats method
- [x] 4.0 Add archive file functionality with configurable filename
  - [x] 4.1 Implement archive file writing functionality
  - [x] 4.2 Add archive file configuration and default filename
  - [x] 4.3 Write summary statistics to archive file
- [x] 5.0 Enhance error handling and verbose error output
  - [x] 5.1 Add graceful error handling for missing attributes
  - [x] 5.2 Implement detailed error output when verbose mode is enabled
  - [x] 5.3 Add error handling for file I/O operations
