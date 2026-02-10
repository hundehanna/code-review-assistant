"""AI-powered code review using OpenAI."""
import os
from pathlib import Path
from typing import List, Optional

from openai import OpenAI

from code_review_assistant.models.review import CodeIssue, ReviewResult, Severity


class AIReviewer:
    """Uses AI to review code and provide feedback."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize AI reviewer.
        
        Args:
            api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY env var
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        self.client = OpenAI(api_key=self.api_key)

    def review_code(self, file_path: Path, max_lines: int = 500) -> List[CodeIssue]:
        """Review code in a file using AI.
        
        Args:
            file_path: Path to the Python file to review
            max_lines: Maximum number of lines to send to AI (to manage costs)
            
        Returns:
            List of CodeIssue objects found by AI
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Limit the number of lines to review to manage API costs
            if len(lines) > max_lines:
                content = ''.join(lines[:max_lines])
                truncated = True
            else:
                content = ''.join(lines)
                truncated = False
            
            prompt = self._build_review_prompt(content, str(file_path), truncated)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Python code reviewer. Provide concise, "
                                   "actionable feedback on code quality, best practices, and potential bugs."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            feedback = response.choices[0].message.content
            issues = self._parse_ai_feedback(feedback, str(file_path))
            
            return issues
            
        except Exception as e:
            return [CodeIssue(
                file_path=str(file_path),
                line_number=0,
                severity=Severity.ERROR,
                message=f"Error during AI review: {str(e)}"
            )]

    def generate_summary(self, review_result: ReviewResult) -> str:
        """Generate a summary of the review results using AI.
        
        Args:
            review_result: The complete review result
            
        Returns:
            A summary string
        """
        try:
            issues_summary = self._format_issues_for_summary(review_result.issues)
            test_summary = self._format_test_results(review_result.test_result)
            
            prompt = f"""Please provide a brief summary (2-3 sentences) of this code review:

Issues Found:
{issues_summary}

Test Results:
{test_summary}

Focus on the most important findings and overall code quality."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert code reviewer. Provide concise summaries."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=200
            )
            
            return response.choices[0].message.content or "Review completed."
            
        except Exception as e:
            return f"Review completed with {len(review_result.issues)} issues found."

    def _build_review_prompt(self, code: str, file_path: str, truncated: bool) -> str:
        """Build the prompt for code review."""
        truncation_note = "\n(Note: File was truncated to first 500 lines)" if truncated else ""
        
        return f"""Review the following Python code from {file_path}{truncation_note}:

```python
{code}
```

Please identify:
1. Potential bugs or errors
2. Code quality issues
3. Best practice violations
4. Security concerns
5. Performance issues

For each issue, provide:
- Line number (if applicable)
- Severity (ERROR, WARNING, or INFO)
- Clear description
- Suggestion for improvement

Format your response as:
LINE <number>: [SEVERITY] Description - Suggestion"""

    def _parse_ai_feedback(self, feedback: str, file_path: str) -> List[CodeIssue]:
        """Parse AI feedback into CodeIssue objects."""
        issues = []
        
        if not feedback:
            return issues
        
        lines = feedback.split('\n')
        for line in lines:
            line = line.strip()
            if not line or not line.startswith('LINE'):
                continue
            
            try:
                # Parse format: LINE 10: [ERROR] Description - Suggestion
                parts = line.split(':', 1)
                if len(parts) < 2:
                    continue
                
                line_num_str = parts[0].replace('LINE', '').strip()
                rest = parts[1].strip()
                
                # Extract severity
                severity = Severity.INFO
                if '[ERROR]' in rest:
                    severity = Severity.ERROR
                    rest = rest.replace('[ERROR]', '').strip()
                elif '[WARNING]' in rest:
                    severity = Severity.WARNING
                    rest = rest.replace('[WARNING]', '').strip()
                elif '[INFO]' in rest:
                    rest = rest.replace('[INFO]', '').strip()
                
                # Split message and suggestion
                message = rest
                suggestion = None
                if ' - ' in rest:
                    message, suggestion = rest.split(' - ', 1)
                
                issues.append(CodeIssue(
                    file_path=file_path,
                    line_number=int(line_num_str),
                    severity=severity,
                    message=message.strip(),
                    suggestion=suggestion.strip() if suggestion else None
                ))
            except (ValueError, IndexError):
                # Skip lines that don't match the expected format
                continue
        
        return issues

    def _format_issues_for_summary(self, issues: List[CodeIssue]) -> str:
        """Format issues for summary generation."""
        if not issues:
            return "No issues found"
        
        errors = sum(1 for i in issues if i.severity == Severity.ERROR)
        warnings = sum(1 for i in issues if i.severity == Severity.WARNING)
        infos = sum(1 for i in issues if i.severity == Severity.INFO)
        
        return f"{errors} errors, {warnings} warnings, {infos} info messages"

    def _format_test_results(self, test_result) -> str:
        """Format test results for summary."""
        if not test_result:
            return "Tests not run"
        
        if test_result.passed:
            return f"All {test_result.passed_tests} tests passed"
        else:
            return f"{test_result.failed_tests} of {test_result.total_tests} tests failed"
