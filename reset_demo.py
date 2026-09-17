from pathlib import Path


DEMO_FILE = (
    Path(__file__).resolve().parent
    / "demo_repo"
    / "calculator.py"
)


BUGGY_CODE = """\
def add(a, b):
    return a + b


def divide(a, b):
    return a * b
"""


def main():
    DEMO_FILE.write_text(
        BUGGY_CODE,
        encoding="utf-8",
    )

    print("Demo repository reset successfully.")
    print(f"Updated: {DEMO_FILE}")


if __name__ == "__main__":
    main()