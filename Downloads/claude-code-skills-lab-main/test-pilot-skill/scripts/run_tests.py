#!/usr/bin/env python3

import subprocess
import sys
import os
from pathlib import Path

def run_python_tests(test_file):
    """Run Python unit tests and return results."""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'unittest', '-v'],
            cwd=Path(test_file).parent,
            capture_output=True,
            text=True
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def run_javascript_tests(test_file):
    """Run JavaScript tests with Jest if available."""
    try:
        # Check if jest is available
        result = subprocess.run(['which', 'jest'], capture_output=True, text=True)
        if result.returncode == 0:
            result = subprocess.run(
                ['jest', test_file, '--verbose'],
                cwd=Path(test_file).parent,
                capture_output=True,
                text=True
            )
            return result.stdout, result.stderr, result.returncode
        else:
            return "", "Jest not found. Install with: npm install -g jest", 1
    except Exception as e:
        return "", str(e), 1

def update_test_report_with_results(original_report_file, test_results):
    """Update the test report with actual test results."""
    if not os.path.exists(original_report_file):
        return

    with open(original_report_file, 'r') as f:
        content = f.read()

    # Add test results to the report
    lines = content.split('\n')

    # Find where to insert test results (after the main content)
    insert_idx = len(lines)

    # Add test results section
    lines.insert(insert_idx, "\n## Test Execution Results")
    lines.insert(insert_idx + 1, "")
    lines.insert(insert_idx + 2, "```\n" + test_results + "\n```")

    # Write updated report
    with open(original_report_file, 'w') as f:
        f.write('\n'.join(lines))

def main():
    if len(sys.argv) < 2:
        print("Usage: run_tests.py <test_file_path>")
        sys.exit(1)

    test_file = sys.argv[1]

    if not os.path.exists(test_file):
        print(f"Error: Test file {test_file} does not exist")
        sys.exit(1)

    # Determine the language based on file extension
    ext = Path(test_file).suffix.lower()

    if ext == '.py':
        stdout, stderr, returncode = run_python_tests(test_file)
        test_results = stdout + stderr
    elif ext in ['.js', '.ts']:
        stdout, stderr, returncode = run_javascript_tests(test_file)
        test_results = stdout + stderr
    else:
        print(f"Error: Unsupported test file type: {ext}")
        sys.exit(1)

    # Update the test report with results
    report_file = "test-report.md"
    update_test_report_with_results(report_file, test_results)

    print("Test execution completed.")
    print(f"Return code: {returncode}")
    print("Test results added to test-report.md")

if __name__ == "__main__":
    main()