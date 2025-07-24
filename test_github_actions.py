import unittest
import tempfile
import os
from github_actions import CallbackModule

class TestGithubActionsCallback(unittest.TestCase):
    def setUp(self):
        self.plugin = CallbackModule()
        self.plugin._display = type('Display', (), {'display': lambda self, msg: None})()

    def test_ok_status_output(self):
        result = type('Result', (), {
            '_task': type('Task', (), {'get_path': lambda self: 'playbook.yml'})(),
            '_host': type('Host', (), {'get_name': lambda self: 'localhost'})(),
        })()
        self.plugin._current_play = 'TestPlay'
        self.plugin._current_task = 'TestTask'
        self.plugin._emit_task_line(result, status='ok')
        self.assertIn('::notice::', self.plugin.archive_lines[-1])

    def test_changed_status_output(self):
        result = type('Result', (), {
            '_task': type('Task', (), {'get_path': lambda self: 'playbook.yml'})(),
            '_host': type('Host', (), {'get_name': lambda self: 'localhost'})(),
        })()
        self.plugin._current_play = 'TestPlay'
        self.plugin._current_task = 'TestTask'
        self.plugin._emit_task_line(result, status='changed')
        self.assertIn('::warning::', self.plugin.archive_lines[-1])

    def test_failed_status_output(self):
        result = type('Result', (), {
            '_task': type('Task', (), {'get_path': lambda self: 'playbook.yml'})(),
            '_host': type('Host', (), {'get_name': lambda self: 'localhost'})(),
        })()
        self.plugin._current_play = 'TestPlay'
        self.plugin._current_task = 'TestTask'
        self.plugin._emit_task_line(result, status='failed')
        self.assertIn('::error::', self.plugin.archive_lines[-1])

    def test_skipped_status_output(self):
        result = type('Result', (), {
            '_task': type('Task', (), {'get_path': lambda self: 'playbook.yml'})(),
            '_host': type('Host', (), {'get_name': lambda self: 'localhost'})(),
        })()
        self.plugin._current_play = 'TestPlay'
        self.plugin._current_task = 'TestTask'
        self.plugin._emit_task_line(result, status='skipped')
        self.assertNotIn('::notice::', self.plugin.archive_lines[-1])
        self.assertNotIn('::warning::', self.plugin.archive_lines[-1])
        self.assertNotIn('::error::', self.plugin.archive_lines[-1])

    def test_statistics_tracking(self):
        result = type('Result', (), {
            '_task': type('Task', (), {'get_path': lambda self: 'playbook.yml'})(),
            '_host': type('Host', (), {'get_name': lambda self: 'localhost'})(),
        })()
        self.plugin._current_play = 'TestPlay'
        
        # Test ok status
        self.plugin._update_stats(result, 'ok')
        self.assertEqual(self.plugin.stats['totals']['ok'], 1)
        self.assertEqual(self.plugin.stats['plays']['TestPlay']['localhost']['ok'], 1)
        
        # Test changed status
        self.plugin._update_stats(result, 'changed')
        self.assertEqual(self.plugin.stats['totals']['changed'], 1)
        self.assertEqual(self.plugin.stats['plays']['TestPlay']['localhost']['changed'], 1)

    def test_archive_file_functionality(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            self.plugin.archive_file = tmp.name
        
        self.plugin.archive_lines = ['test line 1', 'test line 2']
        self.plugin._write_archive_file()
        
        with open(tmp.name, 'r') as f:
            content = f.read()
            self.assertIn('test line 1', content)
            self.assertIn('test line 2', content)
        
        os.unlink(tmp.name)

    def test_verbose_error_output(self):
        self.plugin.verbose = True
        result = type('Result', (), {
            '_task': type('Task', (), {'get_path': lambda self: 'playbook.yml'})(),
            '_host': type('Host', (), {'get_name': lambda self: 'localhost'})(),
            '_result': {'msg': 'Test error message', 'stderr': 'Test stderr'}
        })()
        
        self.plugin._current_play = 'TestPlay'
        self.plugin._current_task = 'TestTask'
        initial_count = len(self.plugin.archive_lines)
        
        self.plugin.v2_runner_on_failed(result)
        
        # Should have added the task line plus error details
        self.assertGreater(len(self.plugin.archive_lines), initial_count + 1)
        error_lines = [line for line in self.plugin.archive_lines if 'Error details' in line]
        self.assertEqual(len(error_lines), 1)

if __name__ == '__main__':
    unittest.main()
