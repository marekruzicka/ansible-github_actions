# PRD: Ansible Callback Plugin for GitHub Actions Workflow Output

## 1. Introduction/Overview
This feature introduces a custom Ansible stdout callback plugin designed to format output for optimal use within GitHub Actions workflows. The goal is to minimize verbosity, prevent output truncation in the GitHub UI, and present only the most relevant information for CI maintainers.

## 2. Goals
- Reduce output verbosity to avoid hitting GitHub Actions UI buffer limits.
- Present actionable, minimal output grouped by play and task.
- Map Ansible message types to GitHub Actions log levels (notice, warning, error).
- Support log folding/collapsing via GitHub Actions group markers.
- Allow configuration for verbosity, especially for detailed fail messages.

## 3. User Stories
- As a CI maintainer, I want to see only the filename, play name, hostname, status message, and task name for each step, so I can quickly identify issues without sifting through excessive logs.
- As a DevOps engineer, I want failed tasks to show detailed error messages when verbose mode is enabled, so I can debug issues efficiently.

## 4. Functional Requirements
1. The plugin must output, for each task:
   - Filename
   - Play name
   - Hostname
   - Ansible status message (ok, changed, failed, skipped, etc.)
   - Task name
2. The plugin must map Ansible status messages to GitHub Actions log levels:
   - ok → notice
   - changed → warning
   - failed → error
3. The plugin must group output by play and by task using GitHub Actions group markers (`::group::` and `::endgroup::`).
4. The plugin must support configuration for verbosity:
   - When verbose is enabled, failed tasks must show detailed error messages.
5. The plugin must support Ansible versions 2.16+.
6. The plugin must handle errors gracefully and not crash the workflow.

## 5. Non-Goals (Out of Scope)
- Support for non-GitHub CI/CD platforms (e.g., GitLab) is not required at this stage.
- Handling of very verbose output or large playbooks is outside the plugin's scope; the plugin only formats output.

## 6. Design Considerations
- Output should use GitHub Actions log folding/collapsing features for plays and tasks.
- Formatting should be clear and concise, using best judgment for readability.
- No color formatting required unless natively supported by GitHub Actions.

## 7. Technical Considerations
- Must be compatible with Ansible 2.16+ (preferably 2.14+).
- Should not introduce new dependencies.
- Should be easily configurable via Ansible callback plugin configuration.

## 8. Success Metrics
- Output does not exceed GitHub Actions UI buffer limits for typical playbooks.
- CI maintainers can quickly identify failed, changed, and successful tasks.
- No plugin-related errors in workflow runs.

## 9. Open Questions
- Should the plugin support additional configuration options (e.g., filtering by host or task)?
  - no
## 10. Additional Requirements
- The plugin must output summary statistics at the end of the run, including counts of ok, changed, failed, and skipped tasks, grouped by play and host.
- The summary must be presented in plain text format.
- The plugin must support writing all output (including summary) to a plain text archive file, with a configurable filename.
