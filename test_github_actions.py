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

    def test_changed_detection_in_ok_result(self):
        """Test that changed=true in result is detected even when reported as 'ok'"""
        result = type('Result', (), {
            '_task': type('Task', (), {'get_path': lambda self: 'playbook.yml'})(),
            '_host': type('Host', (), {'get_name': lambda self: 'localhost'})(),
            '_result': {'changed': True}  # This should trigger changed status
        })()
        self.plugin._current_play = 'TestPlay'
        self.plugin._current_task = 'TestTask'
        
        # Simulate what happens when Ansible reports changed as 'ok'
        self.plugin.v2_runner_on_ok(result)
        
        # Should have detected the change and marked as warning
        self.assertIn('::warning::', self.plugin.archive_lines[-1])
        self.assertEqual(self.plugin.stats['totals']['changed'], 1)
        self.assertEqual(self.plugin.stats['totals']['ok'], 0)

    def test_direct_changed_status_output(self):
        """Test direct v2_runner_on_changed method"""
        result = type('Result', (), {
            '_task': type('Task', (), {'get_path': lambda self: 'playbook.yml'})(),
            '_host': type('Host', (), {'get_name': lambda self: 'localhost'})(),
        })()
        self.plugin._current_play = 'TestPlay'
        self.plugin._current_task = 'TestTask'
        self.plugin.v2_runner_on_changed(result)
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

    def test_smart_grouping_single_host(self):
        """Test smart grouping with single host (should group by play)"""
        self.plugin.grouping_mode = 'smart'
        
        # Mock play with single host
        play = type('Play', (), {
            'get_name': lambda self: 'Test Play',
            'get_hosts': lambda self: ['host1']
        })()
        
        self.plugin.v2_playbook_on_play_start(play)
        self.assertEqual(self.plugin.current_grouping, 'play')
        self.assertTrue(self.plugin._play_group_open)

    def test_smart_grouping_multiple_hosts(self):
        """Test smart grouping with multiple hosts (should group by task)"""
        self.plugin.grouping_mode = 'smart'
        
        # Mock play with multiple hosts
        play = type('Play', (), {
            'get_name': lambda self: 'Test Play',
            'get_hosts': lambda self: ['host1', 'host2', 'host3']
        })()
        
        self.plugin.v2_playbook_on_play_start(play)
        self.assertEqual(self.plugin.current_grouping, 'task')
        self.assertFalse(self.plugin._play_group_open)

    def test_forced_play_grouping(self):
        """Test forced play grouping mode"""
        self.plugin.grouping_mode = 'play'
        
        play = type('Play', (), {
            'get_name': lambda self: 'Test Play',
            'get_hosts': lambda self: ['host1', 'host2']
        })()
        
        self.plugin.v2_playbook_on_play_start(play)
        self.assertEqual(self.plugin.current_grouping, 'play')
        self.assertTrue(self.plugin._play_group_open)

    def test_forced_task_grouping(self):
        """Test forced task grouping mode"""
        self.plugin.grouping_mode = 'task'
        
        play = type('Play', (), {
            'get_name': lambda self: 'Test Play',
            'get_hosts': lambda self: ['host1']
        })()
        
        self.plugin.v2_playbook_on_play_start(play)
        self.assertEqual(self.plugin.current_grouping, 'task')
        self.assertFalse(self.plugin._play_group_open)

if __name__ == '__main__':
    unittest.main()
