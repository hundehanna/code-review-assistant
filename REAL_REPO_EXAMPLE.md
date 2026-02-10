# Real Repository Example

This guide shows you exactly how to use code-review-assistant on your own repository.

## Step-by-Step: Using on Your Repository

### 1. Install the Tool

```bash
# Clone the code-review-assistant repository
cd /path/to/your/workspace
git clone https://github.com/hundehanna/code-review-assistant.git
cd code-review-assistant

# Install dependencies
poetry install
```

### 2. Navigate to Your Project

```bash
# Go back to your project directory
cd /path/to/your/project
```

### 3. Run the Tool

**Option A: Quick Analysis (No Tests)**
```bash
# Analyze a single file
/path/to/code-review-assistant/.venv/bin/python -m code_review_assistant.cli src/myfile.py --no-tests

# Or use poetry run from the tool directory
cd /path/to/code-review-assistant
poetry run code-review /path/to/your/project/src/myfile.py --no-tests
```

**Option B: Full Analysis (With Tests)**
```bash
poetry run code-review /path/to/your/project/src --no-tests
```

**Option C: With AI Review**
```bash
export OPENAI_API_KEY="sk-your-key-here"
poetry run code-review /path/to/your/project/src/myfile.py --ai
```

## Example: Analyzing a Flask Application

Let's say you have a Flask app with this structure:

```
my-flask-app/
├── app.py
├── models.py
├── views.py
└── tests/
    └── test_app.py
```

### Review the Entire Application

```bash
cd /path/to/code-review-assistant
poetry run code-review /path/to/my-flask-app/
```

This will:
1. ✅ Scan all `.py` files in the directory
2. ✅ Run any pytest tests found
3. ✅ Generate a comprehensive report

### Review Just the Models

```bash
poetry run code-review /path/to/my-flask-app/models.py --no-tests
```

## Example: Analyzing a Django Project

For a Django project:

```bash
# Analyze the entire project
poetry run code-review /path/to/django-project/myapp/

# Analyze specific modules
poetry run code-review /path/to/django-project/myapp/models.py --no-tests
poetry run code-review /path/to/django-project/myapp/views.py --no-tests
```

## Example: Pre-Commit Integration

Add to your project's `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Path to code-review-assistant
REVIEW_TOOL="/path/to/code-review-assistant"

# Get staged Python files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')

if [ -n "$STAGED_FILES" ]; then
    echo "Running code review on staged files..."
    cd "$REVIEW_TOOL"
    for file in $STAGED_FILES; do
        poetry run code-review "/path/to/your/project/$file" --no-tests
    done
fi
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

## Example: CI/CD Integration (GitHub Actions)

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

## Common Patterns

### 1. Review Changed Files Only

```bash
# Review files modified in the last commit
git diff --name-only HEAD~1 | grep '\.py$' | xargs poetry run code-review --no-tests
```

### 2. Review Branch Changes

```bash
# Review files changed in current branch vs main
git diff --name-only main | grep '\.py$' | xargs poetry run code-review --no-tests
```

### 3. Daily Code Quality Check

Create a script `daily-review.sh`:

```bash
#!/bin/bash
cd /path/to/code-review-assistant
poetry run code-review /path/to/your/project/src > /tmp/review-$(date +%Y%m%d).txt
cat /tmp/review-$(date +%Y%m%d).txt
```

Schedule with cron:
```
0 9 * * * /path/to/daily-review.sh
```

## Tips for Different Project Types

### Python Package
```bash
poetry run code-review /path/to/mypackage/mypackage/
```

### Script Collection
```bash
poetry run code-review /path/to/scripts/*.py --no-tests
```

### Jupyter Notebooks
Convert notebooks first:
```bash
jupyter nbconvert --to script notebook.ipynb
poetry run code-review notebook.py --no-tests
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

## Next Steps

1. Try it on a small file first
2. Review the output and understand the issues
3. Gradually expand to larger parts of your codebase
4. Integrate into your development workflow
5. Enable AI review for intelligent feedback

For more examples, see [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md).
