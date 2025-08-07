#!/usr/bin/env python3
"""
Test script to demonstrate the adaptive grouping functionality
"""

from github_actions import CallbackModule
import sys

class MockDisplay:
    def __init__(self):
        self.lines = []
    
    def display(self, msg):
        self.lines.append(msg)
        print(msg)

class MockTask:
    def __init__(self, name, path=None):
        self.name = name
        self.path = path
    
    def get_name(self):
        return self.name
    
    def get_path(self):
        return self.path

class MockPlay:
    def __init__(self, name, hosts):
        self.name = name
        self.hosts = hosts
    
    def get_name(self):
        return self.name
    
    def get_hosts(self):
        return self.hosts

class MockHost:
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name

class MockResult:
    def __init__(self, task, host):
        self._task = task
        self._host = host

def test_grouping_mode(mode, hosts, description):
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Mode: {mode}, Hosts: {hosts}")
    print('='*60)
    
    # Create plugin instance
    plugin = CallbackModule()
    plugin.grouping_mode = mode
    display = MockDisplay()
    plugin._display = display
    
    # Mock a play start
    play = MockPlay("Test Play", hosts)
    plugin.v2_playbook_on_play_start(play)
    
    # Mock tasks
    task1 = MockTask("Task 1: Setup", "setup.yml")
    plugin.v2_playbook_on_task_start(task1, False)
    
    # Mock results for each host
    for hostname in hosts:
        host = MockHost(hostname)
        result = MockResult(task1, host)
        plugin.v2_runner_on_ok(result)
    
    task2 = MockTask("Task 2: Configure", "config.yml")
    plugin.v2_playbook_on_task_start(task2, False)
    
    for hostname in hosts:
        host = MockHost(hostname)
        result = MockResult(task2, host)
        plugin.v2_runner_on_changed(result)
    
    # End playbook
    plugin.v2_playbook_on_stats(None)
    
    # Analyze output
    group_starts = [line for line in display.lines if line.startswith('::group::')]
    print(f"\nGroup structure:")
    for group in group_starts:
        print(f"  {group}")
    
    return plugin.current_grouping

def main():
    print("=== Adaptive Grouping Test ===")
    
    # Test scenarios
    scenarios = [
        ('smart', ['host1'], 'Smart mode with single host (should group by play)'),
        ('smart', ['host1', 'host2', 'host3'], 'Smart mode with multiple hosts (should group by task)'),
        ('play', ['host1', 'host2'], 'Force play grouping with multiple hosts'),
        ('task', ['host1'], 'Force task grouping with single host'),
    ]
    
    results = []
    for mode, hosts, description in scenarios:
        grouping = test_grouping_mode(mode, hosts, description)
        results.append((mode, len(hosts), grouping))
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    for mode, host_count, actual_grouping in results:
        print(f"Mode: {mode:5} | Hosts: {host_count} | Actual grouping: {actual_grouping}")

if __name__ == "__main__":
    main()
