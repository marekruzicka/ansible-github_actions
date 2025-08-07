# GitHub Actions Ansible Callback Plugin

A sophisticated Ansible callback plugin that formats output for optimal display in GitHub Actions workflow logs, featuring smart grouping, comprehensive status mapping, and detailed statistics tracking.

## Features

- **Smart Grouping**: Automatically adapts folding strategy based on host count
  - Single host: Groups by play for logical progression view
  - Multiple hosts: Groups by task to show parallel execution clearly
- **GitHub Actions Integration**: Full support for workflow commands (`::group::`, `::notice::`, `::warning::`, `::error::`)
- **Comprehensive Status Mapping**: 
  - `ok` → `::notice::` (blue info)
  - `changed` → `::warning::` (yellow warning)  
  - `failed` → `::error::` (red error)
  - `unreachable` → `::error::` (red error)
  - `skipped` → plain text (no formatting)
- **Statistics Tracking**: Detailed per-play and per-host statistics
- **Archive Support**: Optional output archiving to file
- **Configurable**: Supports both environment variables and ansible.cfg configuration

## Quick Start

1. Copy `github_actions.py` to your project directory
2. Configure in `ansible.cfg`:
   ```ini
   [defaults]
   stdout_callback = github_actions
   callback_plugins = ./

   [callback_github_actions]  
   grouping = smart
   verbose = true
   archive_file = /tmp/ansible_output.log
   ```
3. Run your playbook - output will be automatically formatted for GitHub Actions!

## Configuration Options

### Environment Variables
- `GITHUB_ACTIONS_GROUPING`: `smart` (default), `play`, or `task`
- `GITHUB_ACTIONS_VERBOSE`: `true` or `false` (default)
- `GITHUB_ACTIONS_ARCHIVE_FILE`: Path to archive file (optional)

### ansible.cfg
```ini
[callback_github_actions]
grouping = smart      # Grouping mode
verbose = true        # Enable debug output
archive_file = /tmp/ansible_output.log  # Archive file path
```

## Grouping Modes

### Smart Mode (Recommended)
```bash
# Single host - uses play grouping
ansible-playbook -i host1, playbook.yml

# Multiple hosts - uses task grouping  
ansible-playbook -i host1,host2,host3, playbook.yml
```

- **Single Host**: Groups by play - shows logical flow through configuration steps
- **Multiple Hosts**: Groups by task - shows which hosts completed each step

### Play Mode
Forces play-level grouping regardless of host count. Best for sequential workflows.

### Task Mode  
Forces task-level grouping regardless of host count. Best for parallel operations.

## Testing

The `test/` directory contains comprehensive testing tools:

### Unit Tests
```bash
cd test/
python3 -m pytest test_github_actions.py -v
```

### Live Demo
```bash
cd test/

# Test single host (play grouping)
ansible-playbook -i 127.0.0.1, main.yml

# Test multiple hosts (task grouping)  
ansible-playbook -i 127.0.0.1,127.0.0.2,127.0.0.3, main.yml

# Run full test suite
./run_tests.sh
```

### Test Files
- `test_github_actions.py` - Comprehensive unit tests
- `test_grouping.py` - Grouping functionality tests  
- `test_output.py` - Output formatting tests
- `test_changed_fix.py` - Changed detection tests
- `test_unreachable.py` - Unreachable host tests
- `main.yml` - Demo playbook showcasing features
- `run_tests.sh` - Automated test script

## Example Output

### Single Host (Play Grouping)
```
::group::Play: Deploy Application
::notice::tasks/setup.yml | web-server | ok | Deploy Application | Install packages
::warning::tasks/config.yml | web-server | changed | Deploy Application | Update config
::notice::tasks/service.yml | web-server | ok | Deploy Application | Start service
::endgroup::
```

### Multiple Hosts (Task Grouping)
```
::group::Play: Deploy Application  
::notice::tasks/setup.yml | web-01 | ok | Deploy Application | Install packages
::endgroup::
::group::Install packages
::notice::tasks/setup.yml | web-02 | ok | Deploy Application | Install packages
::notice::tasks/setup.yml | web-03 | ok | Deploy Application | Install packages
::endgroup::
::group::Update config
::warning::tasks/config.yml | web-01 | changed | Deploy Application | Update config
::error::tasks/config.yml | web-02 | unreachable | Deploy Application | Update config
::warning::tasks/config.yml | web-03 | changed | Deploy Application | Update config
::endgroup::
```

## Advanced Usage

### CI/CD Integration
```yaml
# .github/workflows/deploy.yml
- name: Run Ansible Playbook
  run: |
    export GITHUB_ACTIONS_GROUPING=smart
    export GITHUB_ACTIONS_VERBOSE=true
    ansible-playbook -i inventory playbook.yml
```

### Error Handling
The plugin gracefully handles:
- Missing file paths
- Network connectivity issues  
- Invalid task results
- Archive file I/O errors

### Performance
- Minimal overhead - only formats output that would be displayed anyway
- Efficient grouping decisions
- Optional archiving doesn't impact execution speed

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Plugin not loading | Check `callback_plugins` path in ansible.cfg |
| No formatting | Verify `stdout_callback = github_actions` |
| Archive errors | Ensure archive file path is writable |
| Grouping issues | Enable verbose mode for debugging |
| Missing statistics | Check for early playbook termination |

## Contributing

1. Run tests: `cd test && python3 -m pytest test_github_actions.py -v`
2. Test live demo: `cd test && ./run_tests.sh` 
3. Update documentation as needed
4. Submit pull request with test coverage

## License

This project follows standard open source practices. See repository for license details.
