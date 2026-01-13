#!/usr/bin/env python3

import os
import sys
import ast
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

def detect_language(file_path: str) -> str:
    """Detect the programming language based on file extension."""
    ext = Path(file_path).suffix.lower()
    lang_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.cs': 'csharp',
        '.rb': 'ruby',
        '.go': 'go',
        '.rs': 'rust'
    }
    return lang_map.get(ext, 'unknown')

def analyze_python_code(file_path: str) -> Dict:
    """Analyze Python code to extract functions, classes, and methods."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return {"error": "Syntax error in Python file"}

    functions = []
    classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Skip private functions and special methods unless they're part of a class
            if not node.name.startswith('_'):
                func_info = {
                    "name": node.name,
                    "line": node.lineno,
                    "args": [arg.arg for arg in node.args.args if arg.arg != 'self'],
                    "docstring": ast.get_docstring(node),
                    "returns": None  # We could enhance this to detect return hints
                }
                functions.append(func_info)

        elif isinstance(node, ast.AsyncFunctionDef):
            if not node.name.startswith('_'):
                func_info = {
                    "name": node.name,
                    "line": node.lineno,
                    "args": [arg.arg for arg in node.args.args if arg.arg != 'self'],
                    "docstring": ast.get_docstring(node),
                    "returns": None,
                    "async": True
                }
                functions.append(func_info)

        elif isinstance(node, ast.ClassDef):
            class_methods = []
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not item.name.startswith('_') or item.name.startswith('__'):
                        method_info = {
                            "name": item.name,
                            "line": item.lineno,
                            "args": [arg.arg for arg in item.args.args if arg.arg != 'self'],
                            "docstring": ast.get_docstring(item),
                            "returns": None
                        }
                        if isinstance(item, ast.AsyncFunctionDef):
                            method_info["async"] = True
                        class_methods.append(method_info)

            class_info = {
                "name": node.name,
                "line": node.lineno,
                "methods": class_methods,
                "docstring": ast.get_docstring(node)
            }
            classes.append(class_info)

    return {
        "functions": functions,
        "classes": classes,
        "language": "python",
        "file_path": file_path
    }

def generate_python_test_content(code_analysis: Dict) -> str:
    """Generate Python unit test content based on code analysis."""
    test_content = []

    # Import statements
    test_content.append("import unittest")
    test_content.append("from unittest.mock import Mock, patch")
    test_content.append("")

    # Import the original module (assuming same directory)
    original_module = Path(code_analysis["file_path"]).stem
    test_content.append(f"import {original_module}")
    test_content.append("")

    # Create test class
    test_class_name = f"Test{original_module.title().replace('_', '')}"
    test_content.append(f"class {test_class_name}(unittest.TestCase):")
    test_content.append("    def setUp(self):")
    test_content.append("        # Setup code for tests")
    test_content.append("        pass")
    test_content.append("")

    # Generate tests for functions
    for func in code_analysis["functions"]:
        test_content.append(f"    def test_{func['name']}_basic(self):")
        test_content.append(f"        # Test basic functionality of {func['name']}")
        test_content.append(f"        # TODO: Implement actual test for {func['name']}")

        if func['args']:
            # Create mock arguments
            args_list = []
            for arg in func['args']:
                if arg.lower() in ['name', 'title', 'text', 'str']:
                    args_list.append(f"'test_{arg}'")
                elif arg.lower() in ['num', 'count', 'size', 'int']:
                    args_list.append("1")
                elif arg.lower() in ['flag', 'enabled', 'bool']:
                    args_list.append("True")
                else:
                    args_list.append(f"'mock_{arg}'")

            args_str = ", ".join(args_list)
            test_content.append(f"        # result = {original_module}.{func['name']}({args_str})")
            test_content.append(f"        # self.assertIsNotNone(result)")
        else:
            test_content.append(f"        # result = {original_module}.{func['name']}()")
            test_content.append(f"        # self.assertIsNotNone(result)")
        test_content.append("")

        # Additional edge case tests
        test_content.append(f"    def test_{func['name']}_edge_cases(self):")
        test_content.append(f"        # Test edge cases for {func['name']}")
        test_content.append(f"        # TODO: Add edge case tests for {func['name']}")
        test_content.append("")

    # Generate tests for classes
    for cls in code_analysis["classes"]:
        for method in cls["methods"]:
            test_content.append(f"    def test_{cls['name'].lower()}_{method['name']}_basic(self):")
            test_content.append(f"        # Test basic functionality of {cls['name']}.{method['name']}")
            test_content.append(f"        instance = {original_module}.{cls['name']}()")

            if method['args']:
                args_list = []
                for arg in method['args']:
                    if arg.lower() in ['name', 'title', 'text', 'str']:
                        args_list.append(f"'test_{arg}'")
                    elif arg.lower() in ['num', 'count', 'size', 'int']:
                        args_list.append("1")
                    elif arg.lower() in ['flag', 'enabled', 'bool']:
                        args_list.append("True")
                    else:
                        args_list.append(f"'mock_{arg}'")

                args_str = ", ".join(args_list)
                test_content.append(f"        # result = instance.{method['name']}({args_str})")
                test_content.append(f"        # self.assertIsNotNone(result)")
            else:
                test_content.append(f"        # result = instance.{method['name']}()")
                test_content.append(f"        # self.assertIsNotNone(result)")
            test_content.append("")

    test_content.append("")
    test_content.append("if __name__ == '__main__':")
    test_content.append("    unittest.main()")

    return "\n".join(test_content)

def generate_javascript_test_content(code_analysis: Dict) -> str:
    """Generate JavaScript test content using Jest based on code analysis."""
    test_content = []

    # Import statements
    original_file = Path(code_analysis["file_path"]).name
    module_name = Path(code_analysis["file_path"]).stem

    test_content.append(f"const {{ {', '.join([f['name'] for f in code_analysis['functions']])} }} = require('./{module_name}');")
    test_content.append("")

    # Describe block
    test_content.append(f"describe('{module_name}', () => {{")

    # Generate tests for functions
    for func in code_analysis["functions"]:
        test_content.append(f"  describe('{func['name']}', () => {{")
        test_content.append(f"    test('should execute {func['name']} successfully', () => {{")
        test_content.append(f"      // TODO: Implement actual test for {func['name']}")

        if func['args']:
            args_list = []
            for arg in func['args']:
                if arg.lower() in ['name', 'title', 'text', 'str']:
                    args_list.append(f"'test_{arg}'")
                elif arg.lower() in ['num', 'count', 'size', 'int']:
                    args_list.append("1")
                elif arg.lower() in ['flag', 'enabled', 'bool']:
                    args_list.append("true")
                else:
                    args_list.append(f"'mock_{arg}'")

            args_str = ", ".join(args_list)
            test_content.append(f"      // const result = {func['name']}({args_str});")
            test_content.append(f"      // expect(result).toBeDefined();")
        else:
            test_content.append(f"      // const result = {func['name']}();")
            test_content.append(f"      // expect(result).toBeDefined();")

        test_content.append("    });")
        test_content.append("")

        # Edge case test
        test_content.append(f"    test('should handle edge cases for {func['name']}', () => {{")
        test_content.append(f"      // TODO: Add edge case tests for {func['name']}")
        test_content.append("    });")
        test_content.append("  });")
        test_content.append("")

    test_content.append("});")

    return "\n".join(test_content)

def analyze_javascript_code(file_path: str) -> Dict:
    """Analyze JavaScript code to extract functions and classes."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regular expressions to find functions and classes
    # Function declarations: function name() {}, const name = function() {}, const name = () => {}
    func_patterns = [
        r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\([^)]*\)',
        r'const\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*function\s*\([^)]*\)',
        r'const\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*\([^)]*\)\s*=>',
        r'const\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*\w+\s*=>',
        r'let\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*function\s*\([^)]*\)',
        r'let\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*\([^)]*\)\s*=>',
        r'var\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*function\s*\([^)]*\)',
        r'var\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*\([^)]*\)\s*=>'
    ]

    class_pattern = r'class\s+([a-zA-Z_$][a-zA-Z0-9_$]*)'
    method_pattern = r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\([^)]*\)\s*{'

    functions = []
    classes = []

    for pattern in func_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            func_name = match.group(1)
            line_no = content[:match.start()].count('\n') + 1

            # Skip common utility function names that are not user-defined
            if func_name not in ['require', 'console', 'Math', 'Array', 'Object', 'String', 'Number', 'Date', 'Promise']:
                functions.append({
                    "name": func_name,
                    "line": line_no,
                    "args": [],  # Could enhance to extract arguments
                    "docstring": None
                })

    class_matches = re.finditer(class_pattern, content)
    for match in class_matches:
        class_name = match.group(1)
        line_no = content[:match.start()].count('\n') + 1

        # Find methods in this class (simple approach)
        # This is a simplified method extraction - could be enhanced
        class_content_start = match.end()
        # Look for methods until next class or end of file
        class_content = content[class_content_start:]
        brace_count = 0
        class_end_pos = 0

        for i, char in enumerate(class_content):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    class_end_pos = i
                    break

        class_body = class_content[:class_end_pos]
        method_matches = re.finditer(r'\b([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\([^)]*\)\s*{', class_body)

        methods = []
        for m_match in method_matches:
            method_name = m_match.group(1)
            if method_name not in ['constructor']:  # Exclude constructor for simplicity
                method_line = content[:match.start() + class_content_start + m_match.start()].count('\n') + 1
                methods.append({
                    "name": method_name,
                    "line": method_line,
                    "args": [],
                    "docstring": None
                })

        classes.append({
            "name": class_name,
            "line": line_no,
            "methods": methods,
            "docstring": None
        })

    return {
        "functions": functions,
        "classes": classes,
        "language": "javascript",
        "file_path": file_path
    }

def generate_test_report(code_analysis: Dict) -> str:
    """Generate a test report explaining covered test cases."""
    report = []

    report.append(f"# Test Report for {Path(code_analysis['file_path']).name}")
    report.append("")
    report.append(f"This report details the test coverage for the source file: `{code_analysis['file_path']}`")
    report.append("")

    report.append("## Source Code Analysis")
    report.append(f"- Language: {code_analysis.get('language', 'Unknown')}")
    report.append(f"- Total Functions: {len(code_analysis.get('functions', []))}")
    report.append(f"- Total Classes: {len(code_analysis.get('classes', []))}")
    report.append("")

    if code_analysis.get('functions'):
        report.append("## Functions Analyzed")
        report.append("")
        for func in code_analysis['functions']:
            report.append(f"- **{func['name']}** (Line {func['line']})")
            if func.get('docstring'):
                report.append(f"  - Description: {func['docstring'][:100]}{'...' if len(func['docstring']) > 100 else ''}")
            report.append(f"  - Arguments: {len(func['args'])} ({', '.join(func['args']) if func['args'] else 'none'})")
            report.append("")

    if code_analysis.get('classes'):
        report.append("## Classes Analyzed")
        report.append("")
        for cls in code_analysis['classes']:
            report.append(f"- **{cls['name']}** (Line {cls['line']})")
            if cls.get('docstring'):
                report.append(f"  - Description: {cls['docstring'][:100]}{'...' if len(cls['docstring']) > 100 else ''}")
            report.append(f"  - Methods: {len(cls['methods'])}")
            for method in cls['methods']:
                report.append(f"    - {method['name']} (Line {method['line']})")
            report.append("")

    report.append("## Test Coverage Status")
    report.append("- Basic tests: ✅ Generated")
    report.append("- Edge case tests: ⚠️ Manual implementation needed")
    report.append("- Integration tests: ❌ Not implemented")
    report.append("")

    report.append("## Next Steps")
    report.append("1. Review the generated tests")
    report.append("2. Implement the actual test logic in the TODO sections")
    report.append("3. Add more specific assertions based on expected behavior")
    report.append("4. Run the tests to validate functionality")
    report.append("")

    report.append("## Test File Location")
    report.append(f"The test file has been generated as: `{get_test_filename(code_analysis['file_path'], code_analysis['language'])}`")

    return "\n".join(report)

def get_test_filename(source_file: str, language: str) -> str:
    """Generate appropriate test filename based on source file and language."""
    source_path = Path(source_file)
    stem = source_path.stem

    if language == 'python':
        return f"test_{stem}.py"
    elif language in ['javascript', 'typescript']:
        return f"{stem}.test.js"
    else:
        return f"test_{stem}.{source_path.suffix}"

def main():
    if len(sys.argv) < 2:
        print("Usage: generate_tests.py <source_file_path>")
        sys.exit(1)

    source_file = sys.argv[1]

    if not os.path.exists(source_file):
        print(f"Error: File {source_file} does not exist")
        sys.exit(1)

    language = detect_language(source_file)

    if language == 'python':
        code_analysis = analyze_python_code(source_file)
    elif language in ['javascript', 'typescript']:
        code_analysis = analyze_javascript_code(source_file)
    else:
        print(f"Error: Unsupported language for file {source_file}")
        sys.exit(1)

    if "error" in code_analysis:
        print(f"Error analyzing code: {code_analysis['error']}")
        sys.exit(1)

    # Generate test content based on language
    if language == 'python':
        test_content = generate_python_test_content(code_analysis)
    elif language in ['javascript', 'typescript']:
        test_content = generate_javascript_test_content(code_analysis)
    else:
        print(f"Error: Cannot generate tests for unsupported language: {language}")
        sys.exit(1)

    # Write test file
    test_filename = get_test_filename(source_file, language)
    with open(test_filename, 'w', encoding='utf-8') as f:
        f.write(test_content)

    # Generate and write test report
    report_content = generate_test_report(code_analysis)
    report_filename = "test-report.md"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"Generated test file: {test_filename}")
    print(f"Generated test report: {report_filename}")
    print(f"Functions found: {len(code_analysis.get('functions', []))}")
    print(f"Classes found: {len(code_analysis.get('classes', []))}")

if __name__ == "__main__":
    main()