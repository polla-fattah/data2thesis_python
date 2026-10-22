"""Build and synchronize the data2thesis Python package from raw datasets.

Copies the generated case-study data from data/ into data2thesis/src/data2thesis/datasets/
and updates the version metadata.

Usage:
------
python data-raw/build_package.py
"""

from pathlib import Path
import shutil
import re

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
PKG_DIR = ROOT / "data2thesis"
TARGET_DATASETS_DIR = PKG_DIR / "src" / "data2thesis" / "datasets"

DATASETS = [
    "students.csv",
    "questionnaire.csv",
    "semesters.csv",
    "supervisors.csv",
    "open_responses.csv",
    "open_responses_coded.csv",
    "counselling_visits.csv",
    "wellbeing_raw.xlsx",
    "wellbeing.sav",
]


def sync_package():
    TARGET_DATASETS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Copy datasets
    copied = 0
    for filename in DATASETS:
        src = DATA_DIR / filename
        dst = TARGET_DATASETS_DIR / filename
        if src.exists():
            shutil.copy2(src, dst)
            copied += 1
        else:
            print(f"Warning: {src} does not exist.")

    # 2. Sync version
    version_file = DATA_DIR / "VERSION"
    if version_file.exists():
        version = version_file.read_text(encoding="utf-8").strip()

        # Update pyproject.toml
        pyproject_path = PKG_DIR / "pyproject.toml"
        if pyproject_path.exists():
            content = pyproject_path.read_text(encoding="utf-8")
            updated = re.sub(r'version = "[^"]+"', f'version = "{version}"', content, count=1)
            pyproject_path.write_text(updated, encoding="utf-8")

        # Update __init__.py
        init_path = PKG_DIR / "src" / "data2thesis" / "__init__.py"
        if init_path.exists():
            content = init_path.read_text(encoding="utf-8")
            updated = re.sub(r'__version__ = "[^"]+"', f'__version__ = "{version}"', content, count=1)
            init_path.write_text(updated, encoding="utf-8")

        print(f"data2thesis version {version} synchronized: {copied} dataset/example files copied.")
    else:
        print(f"Copied {copied} files.")


if __name__ == "__main__":
    sync_package()
