"""Command-line interface for code review assistant."""
import os
from pathlib import Path
from typing import Optional

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from code_review_assistant.analyzers.ai_reviewer import AIReviewer
from code_review_assistant.analyzers.ast_analyzer import ASTAnalyzer
from code_review_assistant.models.review import ReviewResult, Severity
from code_review_assistant.utils.test_runner import TestRunner

# Load environment variables from .env file
load_dotenv()

console = Console()


def main(
    path: str = typer.Argument(..., help="Path to Python file or directory to review"),
    no_tests: bool = typer.Option(
        False,
        "--no-tests",
        help="Skip running tests as part of the review",
    ),
    use_ai: bool = typer.Option(
        False,
        "--ai",
        help="Use AI-powered review (requires OpenAI API key)",
    ),
    api_key: Optional[str] = typer.Option(
        None,
        help="OpenAI API key (or set OPENAI_API_KEY environment variable)",
    ),
) -> None:
    """Review Python code for issues and provide feedback."""
    # Convert string path to Path object
    path_obj = Path(path)

    if not path_obj.exists():
        console.print(f"[red]Error:[/red] Path '{path}' does not exist")
        raise typer.Exit(1)

    console.print(
        Panel.fit(
            "[bold blue]Code Review Assistant[/bold blue]\n"
            "Analyzing your code for quality and issues...",
            border_style="blue",
        )
    )

    result = ReviewResult()

    # Step 1: AST Analysis
    console.print("\n[bold cyan]Step 1:[/bold cyan] Running AST analysis...")
    analyzer = ASTAnalyzer()

    if path_obj.is_file():
        result.issues.extend(analyzer.analyze_file(path_obj))
    else:
        result.issues.extend(analyzer.analyze_directory(path_obj))

    console.print(f"  Found {len(result.issues)} issues from AST analysis")

    # Step 2: AI Review (optional)
    if use_ai:
        console.print("\n[bold cyan]Step 2:[/bold cyan] Running AI-powered review...")
        try:
            ai_reviewer = AIReviewer(api_key=api_key or os.getenv("OPENAI_API_KEY"))

            if path_obj.is_file():
                ai_issues = ai_reviewer.review_code(path_obj)
                result.issues.extend(ai_issues)
                console.print(f"  Found {len(ai_issues)} additional issues from AI review")
            else:
                console.print("  [yellow]AI review only supports single files currently[/yellow]")
        except ValueError as e:
            console.print(f"  [red]Error:[/red] {e}")
        except Exception as e:
            console.print(f"  [red]Error during AI review:[/red] {e}")

    # Step 3: Run Tests
    if not no_tests:
        console.print("\n[bold cyan]Step 3:[/bold cyan] Running tests...")
        project_path = path_obj if path_obj.is_dir() else path_obj.parent
        test_runner = TestRunner(project_path)
        result.test_result = test_runner.run_tests()

        if result.test_result.passed:
            console.print(f"  [green]✓[/green] All {result.test_result.passed_tests} tests passed")
        elif result.test_result.total_tests == 0:
            console.print("  [yellow]No tests found or pytest not available[/yellow]")
        else:
            console.print(
                f"  [red]✗[/red] {result.test_result.failed_tests} of "
                f"{result.test_result.total_tests} tests failed"
            )

    # Generate AI summary if AI is enabled
    if use_ai and result.issues:
        try:
            ai_reviewer = AIReviewer(api_key=api_key or os.getenv("OPENAI_API_KEY"))
            result.summary = ai_reviewer.generate_summary(result)
        except Exception:
            pass

    # Display Results
    _display_results(result)


def _display_results(result: ReviewResult) -> None:
    """Display review results in a formatted table."""
    console.print("\n" + "=" * 80)
    console.print("[bold]Review Results[/bold]")
    console.print("=" * 80 + "\n")

    if result.summary:
        console.print(Panel(result.summary, title="Summary", border_style="blue"))
        console.print()

    # Test Results
    if result.test_result:
        test_style = "green" if result.test_result.passed else "red"
        test_status = "PASSED" if result.test_result.passed else "FAILED"

        if result.test_result.total_tests > 0:
            console.print(
                f"[bold]Tests:[/bold] [{test_style}]{test_status}[/{test_style}] "
                f"({result.test_result.passed_tests}/{result.test_result.total_tests} passed)\n"
            )
        elif result.test_result.error_message:
            console.print(
                f"[bold]Tests:[/bold] [yellow]{result.test_result.error_message}[/yellow]\n"
            )

    # Issues Table
    if result.issues:
        table = Table(title=f"Issues Found ({len(result.issues)} total)", show_header=True)
        table.add_column("File", style="cyan", no_wrap=False)
        table.add_column("Line", justify="right", style="magenta")
        table.add_column("Severity", justify="center")
        table.add_column("Message", no_wrap=False)

        # Sort by severity (errors first, then warnings, then info)
        severity_order = {Severity.ERROR: 0, Severity.WARNING: 1, Severity.INFO: 2}
        sorted_issues = sorted(result.issues, key=lambda x: severity_order[x.severity])

        for issue in sorted_issues:
            severity_style = {
                Severity.ERROR: "[red]ERROR[/red]",
                Severity.WARNING: "[yellow]WARNING[/yellow]",
                Severity.INFO: "[blue]INFO[/blue]",
            }

            message = issue.message
            if issue.suggestion:
                message += f"\n[dim]→ {issue.suggestion}[/dim]"

            table.add_row(
                Path(issue.file_path).name,
                str(issue.line_number),
                severity_style[issue.severity],
                message,
            )

        console.print(table)
        console.print()

        # Summary counts
        errors = sum(1 for i in result.issues if i.severity == Severity.ERROR)
        warnings = sum(1 for i in result.issues if i.severity == Severity.WARNING)
        infos = sum(1 for i in result.issues if i.severity == Severity.INFO)

        console.print(
            f"[bold]Summary:[/bold] "
            f"[red]{errors} errors[/red], "
            f"[yellow]{warnings} warnings[/yellow], "
            f"[blue]{infos} info[/blue]"
        )
    else:
        console.print("[green]✓ No issues found! Code looks good.[/green]")

    console.print()


# Create the Typer app
app = typer.Typer(add_completion=False)
app.command()(main)


if __name__ == "__main__":
    app()
