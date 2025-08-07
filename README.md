# GitHub Actions Ansible Callback Plugin

## Usage

1. Place `github_actions.py` in your Ansible `callback_plugins` directory.
2. In your `ansible.cfg`, set:
   ```ini
   [defaults]
   stdout_callback = github_actions
   callback_plugins = ./callback_plugins
   ```
3. (Optional) Configure verbosity, archive filename, and grouping:
   ```ini
   [callback_github_actions]
   verbose = true
   archive_file = github_actions_output.txt
   grouping = smart
   ```
   Or set environment variables:
   - `GITHUB_ACTIONS_VERBOSE=true`
   - `GITHUB_ACTIONS_ARCHIVE_FILE=github_actions_output.txt`
   - `GITHUB_ACTIONS_GROUPING=smart`

## Features
- Minimal output: Only filename, play name, hostname, status, and task name per task.
- Smart grouping: Adapts folding strategy based on host count and user preference.
- GitHub Actions log folding: Uses `::group::` and `::endgroup::` for optimal UI organization.
- Status mapping: ok → notice, changed → warning, failed → error.
- Summary statistics: Printed at end of run, grouped by play and host.
- Archive file: All output (including summary) can be written to a plain text file.
- Verbosity: When enabled, failed tasks show detailed error messages.

## Grouping Modes
- **smart** (default): Groups by play for single-host runs, by task for multi-host runs
- **play**: Always groups by play (all tasks within a play are grouped together)
- **task**: Always groups by task (all hosts for each task are grouped together)

The smart mode optimizes for GitHub Actions UI limitations (no nested folding):
- Single host: Play-level grouping shows logical progression through configuration steps
- Multiple hosts: Task-level grouping shows which hosts completed each step

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
