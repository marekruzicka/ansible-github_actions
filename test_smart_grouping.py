#!/usr/bin/env python3
"""
Test script to verify smart grouping works correctly
"""

import os
import tempfile
import yaml

def create_test_inventory():
    """Create a test inventory with multiple hosts"""
    inventory_content = """
[test_hosts]
host1 ansible_connection=local
host2 ansible_connection=local
"""
    fd, path = tempfile.mkstemp(suffix='.ini', prefix='test_inventory_')
    with os.fdopen(fd, 'w') as f:
        f.write(inventory_content)
    return path

def create_test_playbook():
    """Create a simple test playbook"""
    playbook_content = [
        {
            'name': 'Test Smart Grouping',
            'hosts': 'test_hosts',
            'gather_facts': False,
            'tasks': [
                {
                    'name': 'Task 1: Debug message',
                    'debug': {
                        'msg': 'Hello from {{ inventory_hostname }}'
                    }
                },
                {
                    'name': 'Task 2: Set a fact',
                    'set_fact': {
                        'test_var': 'value_from_{{ inventory_hostname }}'
                    }
                }
            ]
        }
    ]
    
    fd, path = tempfile.mkstemp(suffix='.yml', prefix='test_playbook_')
    with os.fdopen(fd, 'w') as f:
        yaml.dump(playbook_content, f, default_flow_style=False)
    return path

def main():
    print("=== Smart Grouping Production Test ===\n")
    
    # Set environment variables for our callback
    os.environ['GITHUB_ACTIONS_GROUPING'] = 'smart'
    os.environ['GITHUB_ACTIONS_VERBOSE'] = 'true'
    os.environ['ANSIBLE_STDOUT_CALLBACK'] = 'github_actions'
    
    # Create temporary files
    inventory_path = create_test_inventory()
    playbook_path = create_test_playbook()
    
    try:
        # Set the callback plugin path
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        os.environ['ANSIBLE_CALLBACK_PLUGINS'] = plugin_dir
        
        # Run ansible-playbook command
        cmd = f"ansible-playbook -i {inventory_path} {playbook_path} -v"
        print(f"Running: {cmd}")
        print("=" * 60)
        
        result = os.system(cmd)
        
        print("=" * 60)
        if result == 0:
            print("✅ Test completed successfully!")
            print("Check the output above to verify smart grouping switched from play to task mode.")
        else:
            print("❌ Test failed with non-zero exit code")
            
    finally:
        # Clean up
        try:
            os.unlink(inventory_path)
            os.unlink(playbook_path)
        except:
            pass

if __name__ == '__main__':
    main()
