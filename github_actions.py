# github_actions.py
"""
Ansible callback plugin for GitHub Actions-compatible output.
Groups output by play and task using ::group:: and ::endgroup:: markers.
"""
from ansible.plugins.callback import CallbackBase

CALLBACK_VERSION = '2.0'
CALLBACK_TYPE = 'stdout'
CALLBACK_NAME = 'github_actions'

class CallbackModule(CallbackBase):
    def __init__(self):
        super(CallbackModule, self).__init__()
        self._current_play = None
        self._current_task = None
        self._group_open = False
        self.archive_lines = []

    def v2_playbook_on_play_start(self, play):
        play_name = play.get_name().strip()
        self._current_play = play_name
        self._display.display(f"::group::Play: {play_name}")
        self.archive_lines.append(f"::group::Play: {play_name}")
        self._group_open = True

    def v2_playbook_on_task_start(self, task, is_conditional):
        task_name = task.get_name().strip()
        self._current_task = task_name
        self._display.display(f"::group::Task: {task_name}")
        self.archive_lines.append(f"::group::Task: {task_name}")

    def v2_runner_on_ok(self, result):
        self._emit_task_line(result, status='ok')

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self._emit_task_line(result, status='failed')

    def v2_runner_on_skipped(self, result):
        self._emit_task_line(result, status='skipped')

    def v2_runner_on_unreachable(self, result):
        self._emit_task_line(result, status='unreachable')

    def v2_playbook_on_stats(self, stats):
        if self._group_open:
            self._display.display("::endgroup::")
            self.archive_lines.append("::endgroup::")
            self._group_open = False

    def _emit_task_line(self, result, status):
        filename = result._task.get_path() or ''
        play_name = self._current_play or ''
        hostname = result._host.get_name() if hasattr(result, '_host') else ''
        task_name = self._current_task or ''
        line = f"{filename} | {play_name} | {hostname} | {status} | {task_name}"
        self._display.display(line)
        self.archive_lines.append(line)

        # End group after each task for GitHub UI folding
        self._display.display("::endgroup::")
        self.archive_lines.append("::endgroup::")
