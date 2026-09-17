import argparse
from pathlib import Path

from repofix import solve_issue


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "RepoFix - AI-powered Python "
            "repository debugging agent"
        )
    )

    parser.add_argument(
        "--repo",
        default="./demo_repo",
        help=(
            "Path to the Python repository "
            "(default: ./demo_repo)"
        ),
    )

    parser.add_argument(
        "--issue",
        default=None,
        help="Bug description.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    repo_path = Path(
        args.repo
    ).resolve()

    print()
    print("=" * 60)
    print("RepoFix Agent")
    print("=" * 60)
    print(f"Repository: {repo_path}")

    issue = args.issue

    if not issue:
        print()
        issue = input(
            "Describe the bug:\n> "
        ).strip()

    if not issue:
        print("Issue cannot be empty.")
        return

    print()
    print(f"Issue: {issue}")
    print("-" * 60)

    try:
        result = solve_issue(
            repo_path,
            issue,
        )

    except Exception as exc:
        print()
        print(
            f"RepoFix failed: "
            f"{type(exc).__name__}: {exc}"
        )
        return

    print()
    print("=" * 60)
    print("Result")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()