import os
import sys
from pathlib import Path

# Find bundled files when running inside PyInstaller.
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)  # type: ignore
else:
    os.chdir(Path(__file__).resolve().parent)

sys.path.insert(0, str(Path.cwd() / "src"))

from banana_shooter import main

if __name__ == "__main__":
    main()
