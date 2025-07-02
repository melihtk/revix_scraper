import subprocess
from pathlib import Path


def main() -> None:
    script = Path(__file__).parent / "run_view.py"
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--windowed",
        "--distpath",
        "dist",
        "--name",
        "revix_scraper",
        str(script),
    ]
    icon = Path("revix.ico")
    if icon.exists():
        cmd.extend(["--icon", str(icon)])
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
