from pathlib import Path

from agents import Agent, Runner
from dotenv import load_dotenv

from repofix.context import RepoContext
from repofix.hooks import RepoFixHooks
from repofix.tools import ALL_TOOLS


load_dotenv()


repo_fix_agent = Agent[RepoContext](
    name="RepoFix",

    instructions="""
You are RepoFix, an autonomous Python debugging agent.

Your goal is to resolve the user's bug report by inspecting
and modifying the provided repository.

Workflow:

1. Inspect the repository structure.
2. Search for code related to the bug.
3. Read relevant source files and tests.
4. Identify the root cause.
5. Make the smallest reasonable code change.
6. Run the test suite.
7. If tests fail, inspect the failure and continue debugging.
8. Finish only when the tests pass or when you cannot safely
   make further progress.

Rules:

- Always inspect code before modifying it.
- Never modify tests merely to make a failing implementation pass.
- Avoid unrelated changes.
- Prefer replace_in_file over broad rewrites.
- Always run tests after modifying code.
- Never claim success unless tests pass.
- Keep the final response concise.
- In the final response, explain:
  1. the root cause,
  2. what file was changed,
  3. whether tests passed.
""",

    tools=ALL_TOOLS,
)


def solve_issue(
    repo_path: str | Path,
    issue: str,
) -> str:

    context = RepoContext(
        repo_root=repo_path
    )

    result = Runner.run_sync(
        repo_fix_agent,
        issue,
        context=context,
        hooks=RepoFixHooks(),

        # Prevent the agent from looping forever.
        max_turns=12,
    )

    return str(result.final_output)