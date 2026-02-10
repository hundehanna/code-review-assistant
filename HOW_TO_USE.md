# How to Use Code Review Assistant on Your Repository

This guide demonstrates exactly how to use the code-review-assistant tool on any Python repository.

## 🎯 Quick Demo (30 Seconds)

### Step 1: Install
```bash
git clone https://github.com/hundehanna/code-review-assistant.git
cd code-review-assistant
poetry install
```

### Step 2: Try the Built-in Demo
```bash
poetry run code-review demo.py --no-tests
```

### Output:
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
┏━━━━━━━━━┳━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ File    ┃ Line ┃ Severity ┃ Message                          ┃
┡━━━━━━━━━╇━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ demo.py │   23 │ WARNING  │ Function too complex (66 nodes)  │
│ demo.py │   15 │ WARNING  │ Bare except clause found         │
│ demo.py │   39 │ WARNING  │ Bare except clause found         │
│ demo.py │    9 │   INFO   │ Missing docstring                │
└─────────┴──────┴──────────┴──────────────────────────────────┘

Summary: 0 errors, 3 warnings, 6 info
```

## 📂 Using on Your Repository

### Example 1: Analyze a Single File
```bash
cd /path/to/code-review-assistant
poetry run code-review /path/to/your/project/myfile.py --no-tests
```

**Real Example Output:**
```python
# Sample file: calculator.py
def add(a, b):
    return a + b

def divide(x, y):
    try:
        return x / y
    except:  # ⚠️ Bare except - will be flagged
        return None

class Calculator:  # ℹ️ Missing docstring - will be flagged
    def process_data(self):
        # Complex logic with many branches
        # ⚠️ May be flagged as too complex
        pass
```

**Tool Output:**
```
Issues Found (7 total)
┏━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ File           ┃ Line ┃ Severity ┃ Message                    ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ calculator.py  │   10 │ WARNING  │ Bare except clause         │
│ calculator.py  │    3 │   INFO   │ Missing docstring          │
│ calculator.py  │   13 │   INFO   │ Class missing docstring    │
└────────────────┴──────┴──────────┴────────────────────────────┘
```

### Example 2: Analyze Entire Project Directory
```bash
poetry run code-review /path/to/your/project/src --no-tests
```

This will:
- ✅ Recursively scan all `.py` files
- ✅ Skip virtual environments (`.venv`, `venv`)
- ✅ Skip build directories (`__pycache__`, `dist`)
- ✅ Generate comprehensive report

### Example 3: With Test Execution
```bash
poetry run code-review /path/to/your/project
```

Output includes test results:
```
Step 3: Running tests...
  ✓ All 21 tests passed

Tests: PASSED (21/21 passed)
```

## 🏗️ Real Repository Examples

### Flask Application
```
my-flask-app/
├── app.py
├── models.py
├── views.py
└── tests/
```

**Command:**
```bash
poetry run code-review /path/to/my-flask-app/
```

### Django Project
```
django-project/
├── myapp/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
└── tests/
```

**Command:**
```bash
poetry run code-review /path/to/django-project/myapp/
```

## 🔧 Integration Examples

### Pre-Commit Hook
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
REVIEW_TOOL="/path/to/code-review-assistant"
cd "$REVIEW_TOOL"
poetry run code-review $(git diff --cached --name-only | grep '\.py$') --no-tests
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
          
      - name: Install
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

## 🎨 What the Tool Finds

### ❌ ERRORS (Critical)
- Syntax errors
- Import errors
- Code that won't run

### ⚠️ WARNINGS (Important)
- Bare except clauses
- Overly complex functions (>50 AST nodes)
- Code smells

### ℹ️ INFO (Suggestions)
- Missing docstrings
- Style improvements
- Best practice recommendations

## 💡 Common Use Cases

### 1. Before Committing
```bash
git diff --name-only | grep '\.py$' | xargs poetry run code-review --no-tests
```

### 2. Review Branch Changes
```bash
git diff --name-only main | grep '\.py$' | xargs poetry run code-review --no-tests
```

### 3. Daily Quality Check
```bash
poetry run code-review /path/to/project/src > review-$(date +%Y%m%d).txt
```

### 4. AI-Powered Review
```bash
export OPENAI_API_KEY="sk-your-key"
poetry run code-review myfile.py --ai
```

## 📊 Real Results from Testing

### Test 1: Demo File
- **Command:** `poetry run code-review demo.py --no-tests`
- **Result:** 9 issues (3 warnings, 6 info)
- **Issues:** Bare excepts, complex function, missing docstrings

### Test 2: Sample Code
- **Command:** `poetry run code-review sample_code.py --no-tests`
- **Result:** 7 issues (2 warnings, 5 info)
- **Issues:** Bare except, complex method, missing docs

### Test 3: Clean Module
- **Command:** `poetry run code-review src/code_review_assistant/models/review.py --no-tests`
- **Result:** 0 issues ✅
- **Message:** "No issues found! Code looks good."

## 📚 Full Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - 30-second demo
- **[USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)** - Detailed examples
- **[REAL_REPO_EXAMPLE.md](REAL_REPO_EXAMPLE.md)** - Integration guides
- **[FEATURES.md](FEATURES.md)** - Feature list
- **[README.md](README.md)** - Main documentation

## 🚀 Start Now

1. **Clone and install:** See step 1 above
2. **Try the demo:** `poetry run code-review demo.py --no-tests`
3. **Use on your code:** `poetry run code-review /your/project --no-tests`
4. **Fix issues:** Address warnings and errors
5. **Integrate:** Add to pre-commit hooks or CI/CD

---

**Questions?** Check the documentation files or run:
```bash
poetry run code-review --help
```
