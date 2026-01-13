---
name: test-pilot
description: Takes a source code file as input and automatically generates a complete unit test suite with test coverage report. Creates test files (test_*.py or *.test.js) and a test-report.md explaining covered test cases. Use when you need to generate unit tests automatically for source code files.
---

# Test-Pilot Skill

This skill takes a source code file as input and automatically generates a complete unit test suite. It creates test files (test_*.py or *.test.js) and a test-report.md explaining the covered test cases.

## Usage

Trigger this skill when you need to:
- Generate unit tests for a source code file
- Achieve comprehensive test coverage automatically
- Create test documentation and reports
- Save time on manual test creation

## Process

1. Analyze the source code file to identify functions, classes, and methods
2. Generate appropriate test cases for different scenarios and edge cases
3. Create test file with unit tests
4. Generate test-report.md with coverage details

## Key Features

- Automatic detection of code language (Python, JavaScript, etc.)
- Generation of appropriate test frameworks (unittest for Python, Jest for JavaScript)
- Coverage of edge cases and logical flows
- Creation of comprehensive test suites
- Generation of test coverage reports

## Scripts

The skill uses helper scripts in the `scripts/` directory to analyze code and generate tests.