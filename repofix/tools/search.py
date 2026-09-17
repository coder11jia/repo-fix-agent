from agents import RunContextWrapper
from agents.decorators import tool

from repofix.context import RepoContext
from repofix.tools.filesystem import (
    is_ignored,
)


SKIPPED_SUFFIXES = {
    ".pyc",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".pdf",
    ".zip",
    ".exe",
}


@tool
def search_code(
    ctx: RunContextWrapper[RepoContext],
    query: str,
) -> str:
    """
    Search text or symbols in repository source files.

    Args:
        query: Function name, class name, text or symbol.
    """

    if not query.strip():
        return "Search query cannot be empty."

    root = ctx.context.repo_root
    matches = []

    for path in root.rglob("*"):

        if not path.is_file():
            continue

        if is_ignored(path, root):
            continue

        if (
            path.suffix.lower()
            in SKIPPED_SUFFIXES
        ):
            continue

        try:
            if path.stat().st_size > 1_000_000:
                continue

            content = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

        except OSError:
            continue

        for line_number, line in enumerate(
            content.splitlines(),
            start=1,
        ):

            if (
                query.lower()
                not in line.lower()
            ):
                continue

            relative = path.relative_to(root)

            matches.append(
                f"{relative}:{line_number}: "
                f"{line.strip()[:300]}"
            )

            if len(matches) >= 30:
                break

        if len(matches) >= 30:
            break

    if not matches:
        return (
            f'No matches found for "{query}".'
        )

    return "\n".join(matches)