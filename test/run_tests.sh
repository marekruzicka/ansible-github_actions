#!/usr/bin/env bash
# GitHub Actions Callback Plugin Test Script
# This script demonstrates smart grouping with different host configurations

set -e

echo "=============================================="
echo "GitHub Actions Callback Plugin Test Script"
echo "=============================================="
echo

# Ensure we're in the test directory
cd "$(dirname "$0")"

# Set environment variables for GitHub Actions simulation
export GITHUB_ACTIONS_GROUPING=smart
export GITHUB_ACTIONS_VERBOSE=true
export GITHUB_ACTIONS_ARCHIVE_FILE=/tmp/ansible_test_output.log

echo "Environment Configuration:"
echo "  GITHUB_ACTIONS_GROUPING: $GITHUB_ACTIONS_GROUPING"
echo "  GITHUB_ACTIONS_VERBOSE: $GITHUB_ACTIONS_VERBOSE"
echo "  GITHUB_ACTIONS_ARCHIVE_FILE: $GITHUB_ACTIONS_ARCHIVE_FILE"
echo

# Test 1: Single host (should use play grouping)
echo "=============================================="
echo "TEST 1: Single Host (Play Grouping Expected)"
echo "=============================================="
echo "Command: ansible-playbook -i 127.0.0.1, main.yml"
echo
ansible-playbook -i 127.0.0.1, main.yml
echo
echo "✅ Single host test completed"
echo

# Wait a moment between tests
sleep 2

# Test 2: Multiple hosts (should use task grouping)
echo "=============================================="
echo "TEST 2: Multiple Hosts (Task Grouping Expected)"
echo "=============================================="
echo "Command: ansible-playbook -i 127.0.0.1,127.0.0.2,127.0.0.3, main.yml"
echo
ansible-playbook -i 127.0.0.1,127.0.0.2,127.0.0.3, main.yml
echo
echo "✅ Multiple hosts test completed"
echo

# Show archived output if it exists
if [ -f "$GITHUB_ACTIONS_ARCHIVE_FILE" ]; then
    echo "=============================================="
    echo "ARCHIVED OUTPUT (last 50 lines)"
    echo "=============================================="
    tail -50 "$GITHUB_ACTIONS_ARCHIVE_FILE"
    echo
fi

echo "=============================================="
echo "All tests completed successfully!"
echo "=============================================="
echo
echo "Summary of what you should have observed:"
echo "1. Single host test: Output grouped by PLAY"
echo "2. Multiple hosts test: Started with play group, then switched to TASK groups"
echo "3. Smart grouping automatically adapted based on host count"
echo
echo "Check the output above to verify the grouping behavior!"
