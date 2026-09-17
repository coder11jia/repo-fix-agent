from pathlib import Path

from agents import RunContextWrapper
from agents.decorators import tool

from repofix.context import RepoContext


IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".idea",
    ".vscode",
    "node_modules",
}


def safe_path(
    context: RepoContext,
    relative_path: str,
) -> Path:
    """
    Resolve a path while preventing access outside
    the repository.
    """

    target = (
        context.repo_root / relative_path
    ).resolve()

    try:
        target.relative_to(
            context.repo_root
        )

    except ValueError as exc:
        raise ValueError(
            "Access outside repository is not allowed."
        ) from exc

    return target


def is_ignored(
    path: Path,
    root: Path,
) -> bool:

    try:
        relative = path.relative_to(root)

    except ValueError:
        return True

    return any(
        part in IGNORED_DIRS
        for part in relative.parts
    )


@tool
def list_files(
    ctx: RunContextWrapper[RepoContext],
) -> str:
    """
    List files in the repository.
    Use this to understand repository structure.
    """

    files = []

    for path in ctx.context.repo_root.rglob("*"):

        if not path.is_file():
            continue

        if is_ignored(
            path,
            ctx.context.repo_root,
        ):
            continue

        files.append(
            str(
                path.relative_to(
                    ctx.context.repo_root
                )
            )
        )

        if len(files) >= 200:
            break

    if not files:
        return "Repository is empty."

    return "\n".join(files)


@tool
def read_file(
    ctx: RunContextWrapper[RepoContext],
    path: str,
) -> str:
    """
    Read a repository text file.

    Args:
        path: Repository-relative path.
    """

    file_path = safe_path(
        ctx.context,
        path,
    )

    if not file_path.exists():
        return f"File does not exist: {path}"

    if not file_path.is_file():
        return f"Not a file: {path}"

    content = file_path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    lines = []

    for number, line in enumerate(
        content.splitlines(),
        start=1,
    ):
        lines.append(
            f"{number:>4} | {line}"
        )

    output = "\n".join(lines)

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

    return output or "[EMPTY FILE]"