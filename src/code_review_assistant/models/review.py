"""Data models for code review results."""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class Severity(Enum):
    """Severity levels for code issues."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class CodeIssue:
    """Represents a code issue found during review."""

    file_path: str
    line_number: int
    severity: Severity
    message: str
    suggestion: Optional[str] = None


@dataclass
class TestResult:
    """Represents the result of running tests."""

    passed: bool
    total_tests: int
    passed_tests: int
    failed_tests: int
    error_message: Optional[str] = None
    output: str = ""


@dataclass
class ReviewResult:
    """Represents the complete review result."""

    issues: List[CodeIssue] = field(default_factory=list)
    test_result: Optional[TestResult] = None
    summary: str = ""

    def has_errors(self) -> bool:
        """Check if there are any error-level issues."""
        return any(issue.severity == Severity.ERROR for issue in self.issues)

    def has_warnings(self) -> bool:
        """Check if there are any warning-level issues."""
        return any(issue.severity == Severity.WARNING for issue in self.issues)
