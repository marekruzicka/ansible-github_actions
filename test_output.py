#!/usr/bin/env python3
"""
Test script to demonstrate the expected GitHub Actions output format
"""

from github_actions import CallbackModule
import sys

class MockDisplay:
    def display(self, msg):
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
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name

class MockHost:
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name

class MockResult:
    def __init__(self, task, host):
        self._task = task
        self._host = host

def main():
    print("=== GitHub Actions Callback Plugin Output Demo ===\n")
    
    # Create plugin instance
    plugin = CallbackModule()
    plugin._display = MockDisplay()
    
    # Mock a play start
    play = MockPlay("Configure Timezone")
    plugin.v2_playbook_on_play_start(play)
    
    # Mock first task start
    task1 = MockTask("Gather 'Timezone'", "timezone.yml")
    plugin.v2_playbook_on_task_start(task1, False)
    
    # Mock multiple host results for this task
    hosts = ["server1.example.com", "server2.example.com", "server3.example.com"]
    for hostname in hosts:
        host = MockHost(hostname)
        result = MockResult(task1, host)
        plugin.v2_runner_on_ok(result)
    
    # Mock second task start
    task2 = MockTask("Set 'Timezone'", "timezone.yml")
    plugin.v2_playbook_on_task_start(task2, False)
    
    # Mock results for second task
    for hostname in hosts:
        host = MockHost(hostname)
        result = MockResult(task2, host)
        plugin.v2_runner_on_changed(result)
    
    # Mock stats (end of playbook)
    plugin.v2_playbook_on_stats(None)
    
    print("\n=== End of Demo ===")
    print("\nIn GitHub Actions, you should see:")
    print("- 'Configure Timezone' as a collapsible group")
    print("- 'Gather Timezone' as a sub-group with 3 host results")
    print("- 'Set Timezone' as a sub-group with 3 host results")
    print("- 'Summary Statistics' as a final group")

if __name__ == "__main__":
    main()
