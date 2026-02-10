# code-review-assistant

AI-powered Python code review tool with AST analysis. This tool helps you automatically review Python code by:
- Analyzing code structure with AST (Abstract Syntax Tree)
- Running tests automatically
- Providing AI-powered feedback (optional, requires OpenAI API key)

## Features

- **AST Analysis**: Detects common code quality issues including:
  - Missing docstrings
  - Overly complex functions
  - Bare except clauses
  - Syntax errors
- **Test Runner**: Automatically runs pytest tests in your project
- **AI Review** (Optional): Get intelligent code feedback using OpenAI's GPT models
- **Rich Terminal Output**: Beautiful, color-coded reports with detailed suggestions

## Installation

### Prerequisites
- Python 3.10 or higher
- Poetry (for dependency management)

### Install from source

```bash
# Clone the repository
git clone https://github.com/hundehanna/code-review-assistant.git
cd code-review-assistant

# Install dependencies
poetry install

# Optional: Set up OpenAI API key for AI-powered reviews
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

> **📚 For detailed examples and real-world usage, see [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)**

### Quick Start

Review a single Python file:
```bash
poetry run code-review path/to/file.py --no-tests
```

Review an entire directory:
```bash
poetry run code-review path/to/project --no-tests
```

### With test execution

Run code review with automatic test execution:
```bash
poetry run code-review path/to/project
```

Skip tests explicitly:
```bash
poetry run code-review path/to/project --no-tests
```

### With AI-powered review

Enable AI review (requires OpenAI API key):
```bash
poetry run code-review path/to/file.py --ai
```

Provide API key directly:
```bash
poetry run code-review path/to/file.py --ai --api-key "your-key"
```

## Example Output

```
╭───────────────────────────────────────────────╮
│ Code Review Assistant                         │
│ Analyzing your code for quality and issues... │
╰───────────────────────────────────────────────╯

Step 1: Running AST analysis...
  Found 3 issues from AST analysis

Step 2: Running tests...
  ✓ All 15 tests passed

================================================================================
Review Results
================================================================================

Tests: PASSED (15/15 passed)

                    Issues Found (3 total)
┏━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ File     ┃ Line ┃ Severity ┃ Message                     ┃
┡━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ utils.py │   42 │ WARNING  │ Bare except clause found    │
│          │      │          │ → Catch specific exceptions │
│ utils.py │   10 │   INFO   │ Missing docstring           │
└──────────┴──────┴──────────┴─────────────────────────────┘

Summary: 0 errors, 1 warnings, 2 info
```

## Development

### Running tests
```bash
poetry run pytest
```

### Code formatting
```bash
poetry run black src/ tests/
```

### Linting
```bash
poetry run ruff check src/ tests/
```

### Type checking
```bash
poetry run mypy src/
```

## Configuration

Create a `.env` file in the project root to set environment variables:

```env
OPENAI_API_KEY=your-api-key-here
```

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
