# GitHub Actions Ansible Callback Plugin

## Usage

1. Place `github_actions.py` in your Ansible `callback_plugins` directory.
2. In your `ansible.cfg`, set:
   ```ini
   [defaults]
   stdout_callback = github_actions
   callback_plugins = ./callback_plugins
   ```
3. (Optional) Configure verbosity and archive filename:
   ```ini
   [callback_github_actions]
   verbose = true
   archive_file = github_actions_output.txt
   ```
   Or set environment variables:
   - `GITHUB_ACTIONS_VERBOSE=true`
   - `GITHUB_ACTIONS_ARCHIVE_FILE=github_actions_output.txt`

## Features
- Minimal output: Only filename, play name, hostname, status, and task name per task.
- GitHub Actions log folding: Uses `::group::` and `::endgroup::` for plays and tasks.
- Status mapping: ok → notice, changed → warning, failed → error.
- Summary statistics: Printed at end of run, grouped by play and host.
- Archive file: All output (including summary) can be written to a plain text file.
- Verbosity: When enabled, failed tasks show detailed error messages.

## Integration with GitHub Actions
- Output is formatted for optimal display in GitHub Actions workflow logs.
- Log folding allows collapsing/expanding plays and tasks in the UI.
- Status markers (`::notice::`, `::warning::`, `::error::`) highlight important events.

## Testing
- Run unit tests with:
  ```bash
  pytest test_github_actions.py
  ```
- Tests cover output formatting, grouping, summary, archive writing, and configuration options.

## Troubleshooting
- If output is missing or not formatted, check plugin path and configuration.
- For file I/O errors, ensure archive file path is writable.
- For unexpected errors, enable verbosity for more details.
