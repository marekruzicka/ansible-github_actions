#!/usr/bin/env python3
"""
Test script to verify unreachable host formatting
"""

import os
import sys
# Add parent directory to path to import the callback module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from github_actions import CallbackModule

class MockHost:
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name

class MockTask:
    def __init__(self, name, path=None):
        self.name = name
        self.path = path
    
    def get_name(self):
        return self.name
    
    def get_path(self):
        return self.path

class MockResult:
    def __init__(self, host, task, result_data=None):
        self._host = host
        self._task = task
        self._result = result_data or {}

def test_status_formatting():
    """Test different status formatting"""
    print("=== Status Formatting Test ===\n")
    
    # Set environment variables
    os.environ['GITHUB_ACTIONS_GROUPING'] = 'task'
    os.environ['GITHUB_ACTIONS_VERBOSE'] = 'false'
    
    plugin = CallbackModule()
    plugin.set_options()
    
    # Create mock objects
    host1 = MockHost("test_host1")
    host2 = MockHost("unreachable_host")
    task = MockTask("Test Task", "test.yml")
    
    # Test different statuses
    statuses = [
        ('ok', 'Test normal ok status'),
        ('changed', 'Test changed status'),
        ('failed', 'Test failed status'),
        ('unreachable', 'Test unreachable status'),
        ('skipped', 'Test skipped status')
    ]
    
    print("Testing status formatting:")
    print("-" * 50)
    
    for status, description in statuses:
        print(f"\n{description}:")
        plugin._current_task = "Test Task"
        plugin._current_play = "Test Play"
        
        if status == 'unreachable':
            result = MockResult(host2, task)
        else:
            result = MockResult(host1, task)
        
        # Capture output by calling _emit_task_line directly
        plugin._emit_task_line(result, status)
        
        # Show the last line that was added
        if plugin.archive_lines:
            print(f"  Output: {plugin.archive_lines[-1]}")

def main():
    test_status_formatting()
    print("\n" + "=" * 60)
    print("✅ Status formatting test completed!")
    print("Verify that 'unreachable' status shows '::error::' prefix")

if __name__ == '__main__':
    main()
