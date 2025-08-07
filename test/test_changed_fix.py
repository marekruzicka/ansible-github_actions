#!/usr/bin/env python3
"""
Test script to verify the changed detection fix
"""

import os
import sys
# Add parent directory to path to import the callback module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from github_actions import CallbackModule

class MockDisplay:
    def display(self, msg):
        print(msg)

class MockTask:
    def get_path(self):
        return 'test.yml'

class MockHost:
    def get_name(self):
        return 'testhost'

class MockResult:
    def __init__(self, changed=False):
        self._task = MockTask()
        self._host = MockHost()
        self._result = {'changed': changed} if changed else {}

def test_changed_detection():
    print("=== Testing Changed Detection Fix ===\n")
    
    plugin = CallbackModule()
    plugin._display = MockDisplay()
    plugin._current_play = "Test Play"
    plugin._current_task = "Test Task"
    
    print("1. Testing normal 'ok' result (no change):")
    result_ok = MockResult(changed=False)
    plugin.v2_runner_on_ok(result_ok)
    print(f"   Stats - OK: {plugin.stats['totals']['ok']}, Changed: {plugin.stats['totals']['changed']}")
    
    print("\n2. Testing 'ok' result with changed=true:")
    result_changed = MockResult(changed=True)
    plugin.v2_runner_on_ok(result_changed)
    print(f"   Stats - OK: {plugin.stats['totals']['ok']}, Changed: {plugin.stats['totals']['changed']}")
    
    print("\n3. Testing direct changed call:")
    result_direct = MockResult()
    plugin.v2_runner_on_changed(result_direct)
    print(f"   Stats - OK: {plugin.stats['totals']['ok']}, Changed: {plugin.stats['totals']['changed']}")
    
    print("\n4. Archive lines (last 3):")
    for line in plugin.archive_lines[-3:]:
        print(f"   {line}")

if __name__ == "__main__":
    test_changed_detection()
