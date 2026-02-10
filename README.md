# code-review-assistant

AI-powered Python code review tool with AST analysis. This tool helps you automatically review Python code by analyzing code structure, running tests, and providing intelligent feedback.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/dependency-poetry-blue)](https://python-poetry.org/)

## Features

- **AST Analysis**: Detects code quality issues including:
  - Missing docstrings
  - Overly complex functions (>50 AST nodes)
  - Bare except clauses
  - Syntax errors
- **Test Runner**: Automatically runs pytest tests and reports results
- **AI Review** (Optional): Get intelligent code feedback using OpenAI's GPT models
- **Rich Terminal Output**: Beautiful, color-coded reports with detailed suggestions

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/hundehanna/code-review-assistant.git
cd code-review-assistant

# Install dependencies
poetry install
```

### Try the Demo

Run the built-in demo to see it in action:

```bash
poetry run code-review demo.py --no-tests
```

You'll see output like this:

```
╭───────────────────────────────────────────────╮
│ Code Review Assistant                         │
│ Analyzing your code for quality and issues... │
╰───────────────────────────────────────────────╯

Step 1: Running AST analysis...
  Found 9 issues from AST analysis

================================================================================
Review Results
================================================================================

                    Issues Found (9 total)
┏━━━━━━━━━┳━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ File    ┃ Line ┃ Severity ┃ Message                     ┃
┡━━━━━━━━━╇━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ demo.py │   23 │ WARNING  │ Function too complex        │
│ demo.py │   15 │ WARNING  │ Bare except clause          │
│ demo.py │    9 │   INFO   │ Missing docstring           │
└─────────┴──────┴──────────┴─────────────────────────────┘

Summary: 0 errors, 3 warnings, 6 info
```

## Usage

### Basic Usage

Analyze a single Python file:
```bash
poetry run code-review path/to/file.py --no-tests
```

Analyze an entire directory:
```bash
poetry run code-review path/to/project --no-tests
```

### With Test Execution

Run code review with automatic test execution:
```bash
poetry run code-review path/to/project
```

Skip tests explicitly:
```bash
poetry run code-review path/to/project --no-tests
```

### With AI-Powered Review

Enable AI review (requires OpenAI API key):
```bash
export OPENAI_API_KEY="your-api-key-here"
poetry run code-review path/to/file.py --ai
```

Or provide the key directly:
```bash
poetry run code-review path/to/file.py --ai --api-key "your-key"
```

## Usage Examples

### Example 1: Analyzing Your Own Repository

```bash
# From the code-review-assistant directory
cd /path/to/code-review-assistant
poetry run code-review /path/to/your/project/src --no-tests
```

### Example 2: Flask Application

For a Flask app with this structure:
```
my-flask-app/
├── app.py
├── models.py
├── views.py
└── tests/
```

Run:
```bash
poetry run code-review /path/to/my-flask-app/
```

### Example 3: Django Project

```bash
# Analyze the entire Django app
poetry run code-review /path/to/django-project/myapp/

# Analyze specific modules
poetry run code-review /path/to/django-project/myapp/models.py --no-tests
```

### Example 4: Review Changed Files Only

```bash
# Review files modified in the last commit
git diff --name-only HEAD~1 | grep '\.py$' | xargs poetry run code-review --no-tests

# Review files changed in current branch vs main
git diff --name-only main | grep '\.py$' | xargs poetry run code-review --no-tests
```

## Integration Examples

### Pre-Commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
cd /path/to/code-review-assistant
poetry run code-review $(git diff --cached --name-only --diff-filter=ACM | grep '\.py$') --no-tests
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

### GitHub Actions CI/CD

Add to `.github/workflows/code-review.yml`:

```yaml
name: Code Review

on: [push, pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          repository: hundehanna/code-review-assistant
          path: code-review-assistant
          
      - name: Install code-review-assistant
        run: |
          cd code-review-assistant
          pip install poetry
          poetry install
          
      - uses: actions/checkout@v3
        with:
          path: my-project
          
      - name: Review Code
        run: |
          cd code-review-assistant
          poetry run code-review ../my-project/src --no-tests
```

### GitLab CI

Add to `.gitlab-ci.yml`:

```yaml
code_review:
  image: python:3.10
  before_script:
    - pip install poetry
    - git clone https://github.com/hundehanna/code-review-assistant.git
    - cd code-review-assistant && poetry install && cd ..
  script:
    - code-review-assistant/.venv/bin/python -m code_review_assistant.cli src/ --no-tests
```

## Understanding the Output

### Severity Levels

- **ERROR** (Red): Critical issues that must be fixed (e.g., syntax errors)
- **WARNING** (Yellow): Important issues that should be addressed (e.g., bare except, complex functions)
- **INFO** (Blue): Suggestions for improvement (e.g., missing docstrings)

### What the Tool Detects

- **Syntax Errors**: Catches broken Python code with line numbers
- **Missing Docstrings**: Identifies functions/classes without documentation
- **Bare Except Clauses**: Warns about catching all exceptions
- **Complex Functions**: Flags functions with >50 AST nodes
- **Test Results**: Reports pass/fail counts from pytest

## Configuration

Create a `.env` file in the project root to set environment variables:

```env
OPENAI_API_KEY=your-api-key-here
```

## Development

### Running Tests

```bash
poetry run pytest
```

### Code Formatting

```bash
poetry run black src/ tests/
```

### Linting

```bash
poetry run ruff check src/ tests/
```

### Type Checking

```bash
poetry run mypy src/
```

## Architecture

```
code-review-assistant/
├── src/code_review_assistant/
│   ├── analyzers/
│   │   ├── ast_analyzer.py    # AST-based code analysis
│   │   └── ai_reviewer.py     # OpenAI integration
│   ├── models/
│   │   └── review.py          # Data models
│   ├── utils/
│   │   └── test_runner.py     # Test execution
│   └── cli.py                 # Command-line interface
└── tests/                     # Test suite
```

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

## Troubleshooting

### "poetry: command not found"
Install poetry first:
```bash
pip install poetry
```

### "No module named code_review_assistant"
Make sure you're in the code-review-assistant directory:
```bash
cd /path/to/code-review-assistant
poetry install
```

### Tests failing
Use `--no-tests` to skip test execution:
```bash
poetry run code-review /path/to/file.py --no-tests
```

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.
