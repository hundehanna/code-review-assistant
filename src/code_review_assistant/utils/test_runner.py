"""Utilities for running tests."""
import subprocess
from pathlib import Path
from typing import Optional

from code_review_assistant.models.review import TestResult


class TestRunner:
    """Runs tests for a Python project."""

    def __init__(self, project_path: Path):
        """Initialize test runner.
        
        Args:
            project_path: Path to the project directory
        """
        self.project_path = project_path

    def run_tests(self) -> TestResult:
        """Run tests using pytest.
        
        Returns:
            TestResult with test execution results
        """
        try:
            # Check if pytest is available
            result = subprocess.run(
                ["python", "-m", "pytest", "--version"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return TestResult(
                    passed=False,
                    total_tests=0,
                    passed_tests=0,
                    failed_tests=0,
                    error_message="pytest is not installed",
                    output="pytest is not available. Install it with: pip install pytest"
                )
            
            # Run tests with pytest
            result = subprocess.run(
                ["python", "-m", "pytest", "-v", "--tb=short"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            output = result.stdout + result.stderr
            
            # Parse pytest output to extract test counts
            total_tests, passed_tests, failed_tests = self._parse_pytest_output(output)
            
            return TestResult(
                passed=result.returncode == 0,
                total_tests=total_tests,
                passed_tests=passed_tests,
                failed_tests=failed_tests,
                error_message=None if result.returncode == 0 else "Some tests failed",
                output=output
            )
            
        except subprocess.TimeoutExpired:
            return TestResult(
                passed=False,
                total_tests=0,
                passed_tests=0,
                failed_tests=0,
                error_message="Tests timed out after 5 minutes",
                output="Test execution exceeded timeout"
            )
        except Exception as e:
            return TestResult(
                passed=False,
                total_tests=0,
                passed_tests=0,
                failed_tests=0,
                error_message=str(e),
                output=f"Error running tests: {str(e)}"
            )

    def _parse_pytest_output(self, output: str) -> tuple[int, int, int]:
        """Parse pytest output to extract test counts.
        
        Args:
            output: pytest output text
            
        Returns:
            Tuple of (total_tests, passed_tests, failed_tests)
        """
        passed = 0
        failed = 0
        
        # Look for patterns like "3 passed", "2 failed"
        import re
        
        passed_match = re.search(r'(\d+) passed', output)
        if passed_match:
            passed = int(passed_match.group(1))
        
        failed_match = re.search(r'(\d+) failed', output)
        if failed_match:
            failed = int(failed_match.group(1))
        
        total = passed + failed
        
        return total, passed, failed
