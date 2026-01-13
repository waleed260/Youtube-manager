# Test-Pilot Skill - Reference Guide

## Overview

The Test-Pilot skill automatically generates comprehensive unit tests for your source code files. It analyzes your code to identify functions, classes, and methods, then creates appropriate test cases with edge cases and logical flows covered.

## Supported Languages

The skill currently supports:
- **Python** - Generates unittest-based tests
- **JavaScript** - Generates Jest-based tests
- **TypeScript** - Generates Jest-based tests (with ts-jest)

More languages can be added by extending the analysis functions.

## Features

### Automatic Code Analysis
- Parses source code to identify functions and classes
- Extracts function signatures and parameters
- Identifies class methods and their signatures
- Preserves documentation when available

### Test Generation
- Creates basic functionality tests
- Generates edge case test templates
- Handles different parameter types appropriately
- Creates class instance tests when applicable

### Test Reporting
- Generates detailed test coverage reports
- Lists all analyzed functions and classes
- Provides status of test implementation
- Suggests next steps for completing tests

## Usage

### Basic Usage
```bash
python scripts/generate_tests.py path/to/your/source_file.py
```

This will generate:
- A test file (e.g., `test_your_source_file.py`)
- A test report (`test-report.md`)

### Supported File Types
- `.py` - Python files
- `.js` - JavaScript files
- `.ts` - TypeScript files

## Generated Test Structure

### Python Tests
- Uses `unittest` framework
- Creates test class with setUp method
- Generates individual test methods for each function
- Includes basic and edge case test templates

### JavaScript Tests
- Uses Jest framework
- Creates describe blocks for modules and functions
- Generates test cases for different scenarios
- Includes assertion templates

## Test Coverage

The skill generates tests that cover:
- Basic functionality of each function/method
- Parameter handling with mock values
- Class instantiation and method calls
- Edge case test templates (manual implementation needed)

## Customization

### Adding New Language Support
To add support for a new language:
1. Add the file extension to the `detect_language` function
2. Create an analysis function similar to `analyze_python_code`
3. Create a test generation function similar to `generate_python_test_content`

### Extending Test Generation
The generated tests include TODO comments where you need to add specific test logic. The templates provide:
- Basic execution tests
- Parameter handling
- Expected behavior assertions

## Best Practices

### Before Using
- Ensure your source code has valid syntax
- Make sure the source file is accessible
- Verify dependencies are available for your language

### After Generation
- Review the generated test templates
- Implement the actual test logic in TODO sections
- Add specific assertions based on expected behavior
- Run the tests to validate functionality

## Troubleshooting

### Syntax Errors
If the skill fails to analyze your code, check for:
- Syntax errors in the source file
- Unsupported language constructs
- Encoding issues

### Missing Tests
If functions aren't being detected:
- Check if they follow standard naming conventions
- Verify they're not private methods (starting with _)
- Ensure they're defined in the global scope or classes

### Test Framework Issues
If generated tests don't run:
- Install required testing frameworks (unittest for Python, Jest for JavaScript)
- Verify the source module can be imported
- Check for circular dependencies