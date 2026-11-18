
from execution.runner import run_code
from execution.leetcode_runner import run_question_tests


def execute_code(language: str, source_code: str, stdin: str = ""):
    """Execute code with custom standard input."""

    return run_code(
        language=language,
        source_code=source_code,
        stdin=stdin,
    )


def execute_question(
    problem_id: str,
    language: str,
    source_code: str,
    mode: str = "samples",
):
    """Execute a LeetCode problem against configured test cases."""

    return run_question_tests(
        slug=problem_id,
        language=language,
        source_code=source_code,
        mode=mode,
    )
