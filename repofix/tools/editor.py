from agents import RunContextWrapper
from agents.decorators import tool

from repofix.context import RepoContext
from repofix.tools.filesystem import (
    safe_path,
)


@tool
def replace_in_file(
    ctx: RunContextWrapper[RepoContext],
    path: str,
    old_text: str,
    new_text: str,
) -> str:
    """
    Replace one exact piece of text in a repository file.

    Args:
        path: Repository-relative file path.
        old_text: Exact existing text.
        new_text: Replacement text.
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

    count = content.count(old_text)

    if count == 0:
        return (
            "Replacement rejected: "
            "old_text was not found."
        )

    if count > 1:
        return (
            "Replacement rejected: "
            f"old_text occurs {count} times. "
            "Provide more surrounding code."
        )

    updated = content.replace(
        old_text,
        new_text,
        1,
    )

    file_path.write_text(
        updated,
        encoding="utf-8",
    )

    return f"Successfully updated {path}."