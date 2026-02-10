# Quick Start Guide - Try It Now!

Want to see the code-review-assistant in action? Here's the fastest way to try it:

## 🚀 30-Second Demo

```bash
# 1. Clone and install (one time)
git clone https://github.com/hundehanna/code-review-assistant.git
cd code-review-assistant
poetry install

# 2. Run the demo!
poetry run code-review demo.py --no-tests
```

You'll see beautiful output like this:

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

## 📝 Try on Your Code

```bash
# Analyze a file
poetry run code-review /path/to/your/file.py --no-tests

# Analyze a directory
poetry run code-review /path/to/your/project/src --no-tests

# With tests
poetry run code-review /path/to/your/project
```

## 📚 Learn More

- **[USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)** - Detailed examples with real output
- **[REAL_REPO_EXAMPLE.md](REAL_REPO_EXAMPLE.md)** - How to use on your actual repositories
- **[FEATURES.md](FEATURES.md)** - Complete feature list
- **[README.md](README.md)** - Full documentation

## 🎯 Common Commands

```bash
# Quick file check (no tests)
poetry run code-review myfile.py --no-tests

# Full directory analysis with tests
poetry run code-review src/

# AI-powered review
export OPENAI_API_KEY="your-key"
poetry run code-review myfile.py --ai

# Review changed files only
git diff --name-only | grep '\.py$' | xargs poetry run code-review --no-tests
```

## 💡 What It Finds

- ❌ **Syntax errors** - Catches broken Python code
- ⚠️  **Code smells** - Bare except clauses, complex functions
- ℹ️  **Best practices** - Missing docstrings, style issues
- ✅ **Test results** - Runs your pytest tests
- 🤖 **AI insights** - Optional intelligent feedback (needs API key)

## 🔧 Integration Examples

### Pre-commit Hook
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
poetry run code-review $(git diff --cached --name-only | grep '\.py$') --no-tests
```

### GitHub Actions
```yaml
- name: Code Review
  run: |
    pip install poetry
    poetry install
    poetry run code-review src/ --no-tests
```

## 🎓 Next Steps

1. **Start small** - Try `demo.py` first
2. **Understand output** - Learn severity levels (ERROR/WARNING/INFO)
3. **Fix issues** - Address warnings and errors first
4. **Regular use** - Integrate into your workflow
5. **AI review** - Enable for intelligent feedback

---

**Ready to improve your code quality? Start with:**
```bash
poetry run code-review demo.py --no-tests
```
