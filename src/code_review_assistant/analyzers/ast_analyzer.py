"""AST analyzer for Python code."""
import ast
from pathlib import Path
from typing import List

from code_review_assistant.models.review import CodeIssue, Severity


class ASTAnalyzer:
    """Analyzes Python code using AST parsing."""

    def analyze_file(self, file_path: Path) -> List[CodeIssue]:
        """Analyze a Python file and return issues found."""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=str(file_path))
            
            # Check for common issues
            issues.extend(self._check_function_complexity(tree, file_path))
            issues.extend(self._check_docstrings(tree, file_path))
            issues.extend(self._check_exception_handling(tree, file_path))
            
        except SyntaxError as e:
            issues.append(CodeIssue(
                file_path=str(file_path),
                line_number=e.lineno or 0,
                severity=Severity.ERROR,
                message=f"Syntax error: {e.msg}",
            ))
        except Exception as e:
            issues.append(CodeIssue(
                file_path=str(file_path),
                line_number=0,
                severity=Severity.ERROR,
                message=f"Error analyzing file: {str(e)}",
            ))
        
        return issues

    def _check_function_complexity(self, tree: ast.AST, file_path: Path) -> List[CodeIssue]:
        """Check for overly complex functions."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Count statements in function
                statements = sum(1 for _ in ast.walk(node))
                if statements > 50:
                    issues.append(CodeIssue(
                        file_path=str(file_path),
                        line_number=node.lineno,
                        severity=Severity.WARNING,
                        message=f"Function '{node.name}' is too complex ({statements} nodes)",
                        suggestion="Consider breaking this function into smaller functions",
                    ))
        
        return issues

    def _check_docstrings(self, tree: ast.AST, file_path: Path) -> List[CodeIssue]:
        """Check for missing docstrings."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    node_type = "Function" if isinstance(node, ast.FunctionDef) else "Class"
                    # Skip private functions/classes
                    if not node.name.startswith('_'):
                        issues.append(CodeIssue(
                            file_path=str(file_path),
                            line_number=node.lineno,
                            severity=Severity.INFO,
                            message=f"{node_type} '{node.name}' is missing a docstring",
                            suggestion="Add a docstring to document the purpose and behavior",
                        ))
        
        return issues

    def _check_exception_handling(self, tree: ast.AST, file_path: Path) -> List[CodeIssue]:
        """Check for bare except clauses."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    issues.append(CodeIssue(
                        file_path=str(file_path),
                        line_number=node.lineno,
                        severity=Severity.WARNING,
                        message="Bare except clause found",
                        suggestion="Catch specific exceptions instead of using bare except",
                    ))
        
        return issues

    def analyze_directory(self, directory: Path) -> List[CodeIssue]:
        """Analyze all Python files in a directory."""
        issues = []
        
        for py_file in directory.rglob("*.py"):
            # Skip virtual environments and common build directories
            if any(part in py_file.parts for part in ['.venv', 'venv', '__pycache__', 'build', 'dist']):
                continue
            
            issues.extend(self.analyze_file(py_file))
        
        return issues
