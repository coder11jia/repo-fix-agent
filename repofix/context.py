from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class RepoContext:
    repo_root: Path | str
    test_timeout: int = 30
    max_output_chars: int = 12_000

    def __post_init__(self):
        self.repo_root = Path(self.repo_root).resolve()

        if not self.repo_root.exists():
            raise FileNotFoundError(
                f"Repository does not exist: {self.repo_root}"
            )

        if not self.repo_root.is_dir():
            raise NotADirectoryError(
                f"Not a directory: {self.repo_root}"
            )