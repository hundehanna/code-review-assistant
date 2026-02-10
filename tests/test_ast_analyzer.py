"""Tests for AST analyzer."""
import tempfile
from pathlib import Path

import pytest

from code_review_assistant.analyzers.ast_analyzer import ASTAnalyzer
from code_review_assistant.models.review import Severity


@pytest.fixture
def analyzer() -> ASTAnalyzer:
    """Create AST analyzer fixture."""
    return ASTAnalyzer()


def test_analyze_valid_file(analyzer: ASTAnalyzer) -> None:
    """Test analyzing a valid Python file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("""
def hello():
    '''A simple function.'''
    return "hello"
""")
        f.flush()
        temp_path = Path(f.name)
    
    try:
        issues = analyzer.analyze_file(temp_path)
        # Valid file should have minimal issues
        assert isinstance(issues, list)
    finally:
        temp_path.unlink()


def test_analyze_syntax_error(analyzer: ASTAnalyzer) -> None:
    """Test analyzing a file with syntax error."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("def broken(\n")
        f.flush()
        temp_path = Path(f.name)
    
    try:
        issues = analyzer.analyze_file(temp_path)
        assert len(issues) > 0
        assert any(issue.severity == Severity.ERROR for issue in issues)
        assert any("syntax" in issue.message.lower() for issue in issues)
    finally:
        temp_path.unlink()


def test_check_missing_docstring(analyzer: ASTAnalyzer) -> None:
    """Test detection of missing docstrings."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("""
def public_function():
    pass

def _private_function():
    pass

class PublicClass:
    pass
""")
        f.flush()
        temp_path = Path(f.name)
    
    try:
        issues = analyzer.analyze_file(temp_path)
        # Should find missing docstrings for public items
        docstring_issues = [i for i in issues if "docstring" in i.message.lower()]
        assert len(docstring_issues) > 0
        # Private function should not generate docstring warning
        assert not any("_private_function" in i.message for i in issues)
    finally:
        temp_path.unlink()


def test_check_bare_except(analyzer: ASTAnalyzer) -> None:
    """Test detection of bare except clauses."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("""
def risky():
    '''Function with bare except.'''
    try:
        dangerous_operation()
    except:
        pass
""")
        f.flush()
        temp_path = Path(f.name)
    
    try:
        issues = analyzer.analyze_file(temp_path)
        bare_except_issues = [i for i in issues if "bare except" in i.message.lower()]
        assert len(bare_except_issues) > 0
        assert all(i.severity == Severity.WARNING for i in bare_except_issues)
    finally:
        temp_path.unlink()


def test_check_function_complexity(analyzer: ASTAnalyzer) -> None:
    """Test detection of overly complex functions."""
    # Create a very complex function
    complex_code = "def complex_function():\n    '''Complex function.'''\n"
    for i in range(30):
        complex_code += f"    x{i} = {i}\n"
        complex_code += f"    if x{i} > 0:\n"
        complex_code += f"        y{i} = x{i} * 2\n"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(complex_code)
        f.flush()
        temp_path = Path(f.name)
    
    try:
        issues = analyzer.analyze_file(temp_path)
        complexity_issues = [i for i in issues if "complex" in i.message.lower()]
        assert len(complexity_issues) > 0
    finally:
        temp_path.unlink()


def test_analyze_directory(analyzer: ASTAnalyzer) -> None:
    """Test analyzing a directory of Python files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create multiple Python files
        (tmp_path / "file1.py").write_text("def func1():\n    '''Doc.'''\n    pass\n")
        (tmp_path / "file2.py").write_text("def func2():\n    '''Doc.'''\n    pass\n")
        
        # Create subdirectory with Python file
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file3.py").write_text("def func3():\n    pass\n")
        
        issues = analyzer.analyze_directory(tmp_path)
        assert isinstance(issues, list)
        # Should find at least the missing docstring in file3.py
        assert len(issues) >= 1


def test_analyze_directory_skips_venv(analyzer: ASTAnalyzer) -> None:
    """Test that analyze_directory skips virtual environment directories."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create a .venv directory with a Python file
        venv_dir = tmp_path / ".venv"
        venv_dir.mkdir()
        (venv_dir / "bad_code.py").write_text("this is not valid python\n")
        
        # Create a regular Python file
        (tmp_path / "good.py").write_text("def good():\n    '''Good.'''\n    pass\n")
        
        # Should not raise error from bad_code.py in .venv
        issues = analyzer.analyze_directory(tmp_path)
        # Should only analyze good.py, not bad_code.py in .venv
        assert all(".venv" not in issue.file_path for issue in issues)
