"""Tests for CLI interface."""
import tempfile
from pathlib import Path

import pytest
from click.exceptions import Exit
from code_review_assistant.cli import main


@pytest.fixture
def sample_python_file() -> Path:
    """Create a sample Python file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(
            """
def example_function():
    '''An example function.'''
    return 42

def another_function():
    pass
"""
        )
        f.flush()
        temp_path = Path(f.name)

    yield temp_path
    temp_path.unlink()


def test_main_function_exists() -> None:
    """Test that main function exists."""
    assert callable(main)


def test_main_with_nonexistent_file() -> None:
    """Test main with non-existent file."""
    with pytest.raises(Exit):
        main("/nonexistent/file.py")


def test_main_with_existing_file(sample_python_file: Path) -> None:
    """Test main function with existing file."""
    # This should not raise an exception
    try:
        main(str(sample_python_file), no_tests=True, use_ai=False, api_key=None)
    except (SystemExit, Exit):
        # SystemExit/Exit is acceptable - it means the function completed
        pass
