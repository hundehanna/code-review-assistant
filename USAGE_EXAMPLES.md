# Usage Examples - Code Review Assistant

This document shows practical, real-world examples of using the code-review-assistant tool on Python projects.

## Quick Start

The code-review-assistant is a command-line tool that analyzes Python code for quality issues, runs tests, and optionally provides AI-powered feedback.

### Installation

```bash
git clone https://github.com/hundehanna/code-review-assistant.git
cd code-review-assistant
poetry install
```

## Example 1: Analyzing a Single Python File

Let's create a sample Python file with some common issues:

```python
# sample_code.py
def add_numbers(a, b):
    return a + b

def divide_numbers(x, y):
    try:
        result = x / y
        return result
    except:
        return None

class DataProcessor:
    def __init__(self):
        self.data = []
    
    def process_data(self):
        result = []
        for item in self.data:
            if item > 0:
                result.append(item * 2)
            elif item < 0:
                result.append(item / 2)
            else:
                result.append(0)
        return result
```

### Run the Review

```bash
poetry run code-review sample_code.py --no-tests
```

### Output

```
╭───────────────────────────────────────────────╮
│ Code Review Assistant                         │
│ Analyzing your code for quality and issues... │
╰───────────────────────────────────────────────╯

Step 1: Running AST analysis...
  Found 7 issues from AST analysis

================================================================================
Review Results
================================================================================

                    Issues Found (7 total)                    
┏━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ File           ┃ Line ┃ Severity ┃ Message                          ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ sample_code.py │   17 │ WARNING  │ Function 'process_data' is too   │
│                │      │          │ complex (59 nodes)               │
│                │      │          │ → Consider breaking into smaller │
│                │      │          │   functions                      │
│ sample_code.py │   10 │ WARNING  │ Bare except clause found         │
│                │      │          │ → Catch specific exceptions      │
│ sample_code.py │    3 │   INFO   │ Function 'add_numbers' missing   │
│                │      │          │ docstring                        │
│ sample_code.py │    6 │   INFO   │ Function 'divide_numbers'        │
│                │      │          │ missing docstring                │
│ sample_code.py │   13 │   INFO   │ Class 'DataProcessor' missing    │
│                │      │          │ docstring                        │
└────────────────┴──────┴──────────┴──────────────────────────────────┘

Summary: 0 errors, 2 warnings, 5 info
```

### What the Tool Found

1. **WARNING** - Bare except clause (line 10): The generic `except:` should catch specific exceptions
2. **WARNING** - Complex function (line 17): The `process_data` method has too many AST nodes
3. **INFO** - Missing docstrings: Several functions and classes lack documentation

## Example 2: Analyzing an Entire Project Directory

You can analyze all Python files in a directory:

```bash
poetry run code-review src/myproject --no-tests
```

The tool will:
- Recursively scan all `.py` files
- Skip virtual environments (`.venv`, `venv`)
- Skip build directories (`__pycache__`, `build`, `dist`)
- Aggregate all findings into a single report

## Example 3: Running with Tests

If your project has pytest tests, you can include test execution:

```bash
poetry run code-review src/myproject
```

Output includes test results:

```
Step 3: Running tests...
  ✓ All 15 tests passed

Tests: PASSED (15/15 passed)
```

## Example 4: Using AI-Powered Review

For intelligent feedback using GPT models, set your OpenAI API key:

```bash
export OPENAI_API_KEY="sk-your-api-key-here"
poetry run code-review myfile.py --ai
```

The AI review will:
- Identify potential bugs
- Suggest security improvements
- Recommend best practices
- Provide actionable suggestions

## Example 5: Analyzing the Code Review Assistant Itself

You can even use the tool on itself!

```bash
# Analyze the models module
poetry run code-review src/code_review_assistant/models/review.py --no-tests
```

Output:
```
✓ No issues found! Code looks good.
```

```bash
# Analyze the entire project
poetry run code-review src/code_review_assistant --no-tests
```

This will identify any code quality issues in the tool itself.

## Common Use Cases

### 1. Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
poetry run code-review $(git diff --cached --name-only --diff-filter=ACM | grep '\.py$') --no-tests
```

### 2. CI/CD Integration

Add to your GitHub Actions workflow:

```yaml
- name: Code Review
  run: |
    pip install poetry
    poetry install
    poetry run code-review src/ --no-tests
```

### 3. Quick Local Check

Before pushing code:

```bash
# Quick check without tests
poetry run code-review src/ --no-tests

# Full review with tests
poetry run code-review src/
```

### 4. Review Changed Files

```bash
# Review only modified files
git diff --name-only | grep '\.py$' | xargs poetry run code-review --no-tests
```

## Understanding the Output

### Severity Levels

- **ERROR** (Red): Critical issues that must be fixed (e.g., syntax errors)
- **WARNING** (Yellow): Important issues that should be addressed (e.g., bare except, complex functions)
- **INFO** (Blue): Suggestions for improvement (e.g., missing docstrings)

### Issue Details

Each issue includes:
- File name and line number
- Severity level
- Clear description of the problem
- Actionable suggestion for fixing it

## Tips

1. **Start Small**: Begin with a single file to understand the output
2. **Use --no-tests**: Skip test execution when you just want static analysis
3. **Regular Reviews**: Run the tool frequently during development
4. **Focus on Warnings**: Address ERROR and WARNING issues first
5. **Document Code**: Add docstrings to eliminate INFO messages

## Command Reference

```bash
# Basic syntax
poetry run code-review <path> [options]

# Options
--no-tests        Skip test execution
--ai              Enable AI-powered review (requires OpenAI API key)
--api-key KEY     Provide OpenAI API key directly
--help            Show help message
```

## Next Steps

1. Try running the tool on your own projects
2. Configure it in your CI/CD pipeline
3. Use it as part of your code review process
4. Enable AI review for intelligent feedback

For more details, see the main [README.md](README.md) and [FEATURES.md](FEATURES.md).
