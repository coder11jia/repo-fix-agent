import subprocess
import sys

from agents import RunContextWrapper
from agents.decorators import tool

from repofix.context import RepoContext


@tool
def run_tests(
    ctx: RunContextWrapper[RepoContext],
) -> str:
    """
    Run the repository pytest suite.

    Always use this after modifying code.
    """

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
            ],
            cwd=ctx.context.repo_root,
            capture_output=True,
            text=True,
            timeout=ctx.context.test_timeout,
            shell=False,
        )

    except subprocess.TimeoutExpired:
        return (
            "Tests failed because execution "
            f"exceeded {ctx.context.test_timeout} seconds."
        )

    output = (
        f"Return code: {result.returncode}\n\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

    if (
        len(output)
        > ctx.context.max_output_chars
    ):
        output = (
            output[
                :ctx.context.max_output_chars
            ]
            + "\n[OUTPUT TRUNCATED]"
        )

    return output