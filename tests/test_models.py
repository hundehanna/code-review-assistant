"""Tests for review models."""
import pytest

from code_review_assistant.models.review import CodeIssue, ReviewResult, Severity, TestResult


def test_severity_enum() -> None:
    """Test Severity enum values."""
    assert Severity.INFO.value == "info"
    assert Severity.WARNING.value == "warning"
    assert Severity.ERROR.value == "error"


def test_code_issue_creation() -> None:
    """Test CodeIssue creation."""
    issue = CodeIssue(
        file_path="test.py",
        line_number=10,
        severity=Severity.ERROR,
        message="Test error",
        suggestion="Fix it"
    )
    assert issue.file_path == "test.py"
    assert issue.line_number == 10
    assert issue.severity == Severity.ERROR
    assert issue.message == "Test error"
    assert issue.suggestion == "Fix it"


def test_code_issue_without_suggestion() -> None:
    """Test CodeIssue creation without suggestion."""
    issue = CodeIssue(
        file_path="test.py",
        line_number=10,
        severity=Severity.WARNING,
        message="Test warning"
    )
    assert issue.suggestion is None


def test_test_result_passed() -> None:
    """Test TestResult for passing tests."""
    result = TestResult(
        passed=True,
        total_tests=5,
        passed_tests=5,
        failed_tests=0,
        output="All tests passed"
    )
    assert result.passed is True
    assert result.total_tests == 5
    assert result.passed_tests == 5
    assert result.failed_tests == 0
    assert result.error_message is None


def test_test_result_failed() -> None:
    """Test TestResult for failing tests."""
    result = TestResult(
        passed=False,
        total_tests=5,
        passed_tests=3,
        failed_tests=2,
        error_message="Some tests failed",
        output="Test output"
    )
    assert result.passed is False
    assert result.failed_tests == 2
    assert result.error_message == "Some tests failed"


def test_review_result_default() -> None:
    """Test ReviewResult with defaults."""
    result = ReviewResult()
    assert result.issues == []
    assert result.test_result is None
    assert result.summary == ""


def test_review_result_has_errors() -> None:
    """Test has_errors method."""
    result = ReviewResult()
    assert result.has_errors() is False
    
    result.issues.append(CodeIssue(
        file_path="test.py",
        line_number=1,
        severity=Severity.WARNING,
        message="Warning"
    ))
    assert result.has_errors() is False
    
    result.issues.append(CodeIssue(
        file_path="test.py",
        line_number=2,
        severity=Severity.ERROR,
        message="Error"
    ))
    assert result.has_errors() is True


def test_review_result_has_warnings() -> None:
    """Test has_warnings method."""
    result = ReviewResult()
    assert result.has_warnings() is False
    
    result.issues.append(CodeIssue(
        file_path="test.py",
        line_number=1,
        severity=Severity.INFO,
        message="Info"
    ))
    assert result.has_warnings() is False
    
    result.issues.append(CodeIssue(
        file_path="test.py",
        line_number=2,
        severity=Severity.WARNING,
        message="Warning"
    ))
    assert result.has_warnings() is True
