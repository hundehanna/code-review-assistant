"""Tests for test runner utility."""
import tempfile
from pathlib import Path

import pytest

from code_review_assistant.utils.test_runner import TestRunner


@pytest.fixture
def temp_project() -> Path:
    """Create a temporary project directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_parse_pytest_output() -> None:
    """Test parsing pytest output."""
    runner = TestRunner(Path("."))
    
    # Test output with passed tests
    output = "===== 5 passed in 0.23s ====="
    total, passed, failed = runner._parse_pytest_output(output)
    assert total == 5
    assert passed == 5
    assert failed == 0
    
    # Test output with failed tests
    output = "===== 3 passed, 2 failed in 1.23s ====="
    total, passed, failed = runner._parse_pytest_output(output)
    assert total == 5
    assert passed == 3
    assert failed == 2
    
    # Test output with no matches
    output = "No tests collected"
    total, passed, failed = runner._parse_pytest_output(output)
    assert total == 0
    assert passed == 0
    assert failed == 0


def test_test_runner_initialization(temp_project: Path) -> None:
    """Test TestRunner initialization."""
    runner = TestRunner(temp_project)
    assert runner.project_path == temp_project


def test_run_tests_creates_result(temp_project: Path) -> None:
    """Test that run_tests returns a TestResult."""
    runner = TestRunner(temp_project)
    result = runner.run_tests()
    
    assert result is not None
    assert hasattr(result, 'passed')
    assert hasattr(result, 'total_tests')
    assert hasattr(result, 'passed_tests')
    assert hasattr(result, 'failed_tests')
