# github_actions.py
"""
Ansible callback plugin for GitHub Actions-compatible output.
Groups output by play and task using ::group:: and ::endgroup:: markers.
"""
from ansible.plugins.callback import CallbackBase
import os

CALLBACK_VERSION = '2.0'
CALLBACK_TYPE = 'stdout'
CALLBACK_NAME = 'github_actions'

# Default configuration options
DEFAULT_CONFIG = {
    'verbose': False,
    'archive_file': 'ansible-github-actions.log',
    'grouping': 'smart'  # smart, play, task
}

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'github_actions'
    CALLBACK_NEEDS_WHITELIST = True
    
    def __init__(self):
        super(CallbackModule, self).__init__()
        self._current_play = None
        self._current_task = None
        self._play_group_open = False
        self._task_group_open = False
        self.archive_lines = []
        
        # Grouping strategy
        self.grouping_mode = 'smart'  # Will be determined per play for smart mode
        self.current_grouping = None  # 'play' or 'task' for current execution
        
        # Statistics tracking
        self.stats = {
            'plays': {},  # play_name: {host: {ok: 0, changed: 0, failed: 0, skipped: 0, unreachable: 0}}
            'totals': {'ok': 0, 'changed': 0, 'failed': 0, 'skipped': 0, 'unreachable': 0}
        }
        
        # Configuration options with fallbacks
        try:
            self.verbose = self.get_option('verbose')
            self.archive_file = self.get_option('archive_file')
            self.grouping_mode = self.get_option('grouping')
        except:
            self.verbose = DEFAULT_CONFIG['verbose']
            self.archive_file = DEFAULT_CONFIG['archive_file']
            self.grouping_mode = DEFAULT_CONFIG['grouping']

    def set_options(self, task_keys=None, var_options=None, direct=None):
        super(CallbackModule, self).set_options(task_keys=task_keys, var_options=var_options, direct=direct)
        try:
            self.verbose = self.get_option('verbose')
            self.archive_file = self.get_option('archive_file')
            self.grouping_mode = self.get_option('grouping')
        except:
            self.verbose = DEFAULT_CONFIG['verbose']
            self.archive_file = DEFAULT_CONFIG['archive_file']
            self.grouping_mode = DEFAULT_CONFIG['grouping']

    def v2_playbook_on_play_start(self, play):
        # Close previous play group if open
        if self._play_group_open:
            self._display.display("::endgroup::")
            self.archive_lines.append("::endgroup::")
            self._play_group_open = False
        
        play_name = play.get_name().strip()
        self._current_play = play_name
        
        # Determine grouping strategy for this play
        if self.grouping_mode == 'smart':
            # Count hosts in this play
            host_count = len(play.get_hosts()) if hasattr(play, 'get_hosts') else 1
            self.current_grouping = 'play' if host_count == 1 else 'task'
        elif self.grouping_mode == 'play':
            self.current_grouping = 'play'
        elif self.grouping_mode == 'task':
            self.current_grouping = 'task'
        else:
            # Fallback to task grouping for unknown modes
            self.current_grouping = 'task'
        
        # Start play group only if grouping by play
        if self.current_grouping == 'play':
            self._display.display(f"::group::Play: {play_name}")
            self.archive_lines.append(f"::group::Play: {play_name}")
            self._play_group_open = True

    def v2_playbook_on_task_start(self, task, is_conditional):
        # Close previous task group if open
        if self._task_group_open:
            self._display.display("::endgroup::")
            self.archive_lines.append("::endgroup::")
            self._task_group_open = False
        
        task_name = task.get_name().strip()
        self._current_task = task_name
        
        # Start task group only if grouping by task
        if self.current_grouping == 'task':
            self._display.display(f"::group::{task_name}")
            self.archive_lines.append(f"::group::{task_name}")
            self._task_group_open = True

    def v2_runner_on_ok(self, result):
        # Check if this is actually a changed result reported as ok
        actual_status = 'ok'
        if hasattr(result, '_result') and result._result:
            if result._result.get('changed', False):
                actual_status = 'changed'
                self._update_stats(result, 'changed')
            else:
                self._update_stats(result, 'ok')
        else:
            self._update_stats(result, 'ok')
        
        self._emit_task_line(result, status=actual_status)

    def v2_runner_on_changed(self, result):
        self._emit_task_line(result, status='changed')
        self._update_stats(result, 'changed')

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self._emit_task_line(result, status='failed')
        self._update_stats(result, 'failed')
        
        # Show detailed error message if verbose mode is enabled
        if self.verbose and hasattr(result, '_result'):
            error_msg = result._result.get('msg', '')
            if error_msg:
                self._display.display(f"::error::Error details: {error_msg}")
                self.archive_lines.append(f"::error::Error details: {error_msg}")
            
            # Include stderr if available
            stderr = result._result.get('stderr', '')
            if stderr:
                self._display.display(f"::error::STDERR: {stderr}")
                self.archive_lines.append(f"::error::STDERR: {stderr}")

    def v2_runner_on_skipped(self, result):
        self._emit_task_line(result, status='skipped')
        self._update_stats(result, 'skipped')

    def v2_runner_on_unreachable(self, result):
        self._emit_task_line(result, status='unreachable')
        self._update_stats(result, 'unreachable')

    def v2_playbook_on_stats(self, stats):
        # Close any open task group
        if self._task_group_open:
            self._display.display("::endgroup::")
            self.archive_lines.append("::endgroup::")
            self._task_group_open = False
        
        # Close any open play group
        if self._play_group_open:
            self._display.display("::endgroup::")
            self.archive_lines.append("::endgroup::")
            self._play_group_open = False
        
        # Generate summary statistics
        self._display.display("::group::Summary Statistics")
        self.archive_lines.append("::group::Summary Statistics")
        
        # Overall totals
        summary_line = f"Total: {self.stats['totals']['ok']} ok, {self.stats['totals']['changed']} changed, {self.stats['totals']['failed']} failed, {self.stats['totals']['skipped']} skipped, {self.stats['totals']['unreachable']} unreachable"
        self._display.display(summary_line)
        self.archive_lines.append(summary_line)
        
        # Show grouping mode info
        mode_info = f"Grouping mode: {self.grouping_mode}"
        if self.grouping_mode == 'smart':
            mode_info += f" (using {self.current_grouping} grouping)"
        self._display.display(mode_info)
        self.archive_lines.append(mode_info)
        
        # Per-play breakdown
        for play_name, play_stats in self.stats['plays'].items():
            self._display.display(f"\nPlay: {play_name}")
            self.archive_lines.append(f"\nPlay: {play_name}")
            
            for hostname, host_stats in play_stats.items():
                host_line = f"  {hostname}: {host_stats['ok']} ok, {host_stats['changed']} changed, {host_stats['failed']} failed, {host_stats['skipped']} skipped, {host_stats['unreachable']} unreachable"
                self._display.display(host_line)
                self.archive_lines.append(host_line)
        
        self._display.display("::endgroup::")
        self.archive_lines.append("::endgroup::")
        
        # Write archive file
        self._write_archive_file()

    def _write_archive_file(self):
        """Write all collected output to the archive file."""
        try:
            with open(self.archive_file, 'w', encoding='utf-8') as f:
                for line in self.archive_lines:
                    f.write(line + '\n')
        except Exception as e:
            # Use notice level to avoid breaking the workflow
            error_msg = f"::notice::Failed to write archive file {self.archive_file}: {str(e)}"
            self._display.display(error_msg)

    def _emit_task_line(self, result, status):
        try:
            filename = os.path.basename(result._task.get_path() or '') if hasattr(result, '_task') and result._task else ''
            play_name = self._current_play or ''
            hostname = result._host.get_name() if hasattr(result, '_host') and result._host else 'unknown'
            task_name = self._current_task or ''
            
            # Debug: Check for changed flag in verbose mode
            if self.verbose and hasattr(result, '_result') and result._result:
                changed_flag = result._result.get('changed', False)
                if changed_flag and status == 'ok':
                    debug_line = f"::notice::DEBUG: Task reported changed=true but status=ok for {task_name}"
                    self._display.display(debug_line)
                    self.archive_lines.append(debug_line)
            
            # Format: filename | hostname | status | play_name | task_name
            line = f"{filename} | {hostname} | {status} | {play_name} | {task_name}"
            
            # Apply GitHub Actions status marker
            if status == 'ok':
                output_line = f"::notice::{line}"
            elif status == 'changed':
                output_line = f"::warning::{line}"
            elif status == 'failed':
                output_line = f"::error::{line}"
            else:
                output_line = line
                
            self._display.display(output_line)
            self.archive_lines.append(output_line)
        except Exception as e:
            # Fallback error message
            error_line = f"::error::Failed to format task line: {str(e)}"
            self._display.display(error_line)
            self.archive_lines.append(error_line)

    def _update_stats(self, result, status):
        """Update statistics for the given result and status."""
        try:
            hostname = result._host.get_name() if hasattr(result, '_host') and result._host else 'unknown'
            play_name = self._current_play or 'unknown'
            
            # Initialize play stats if needed
            if play_name not in self.stats['plays']:
                self.stats['plays'][play_name] = {}
            
            # Initialize host stats for this play if needed
            if hostname not in self.stats['plays'][play_name]:
                self.stats['plays'][play_name][hostname] = {
                    'ok': 0, 'changed': 0, 'failed': 0, 'skipped': 0, 'unreachable': 0
                }
            
            # Update counters
            if status in self.stats['plays'][play_name][hostname]:
                self.stats['plays'][play_name][hostname][status] += 1
            
            if status in self.stats['totals']:
                self.stats['totals'][status] += 1
        except Exception as e:
            # Log error but don't break execution
            error_msg = f"::notice::Failed to update statistics: {str(e)}"
            self._display.display(error_msg)
            self.archive_lines.append(error_msg)
