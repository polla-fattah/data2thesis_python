"""Build the downloadable project zip files for each playground chapter.

Scans playground-src/chapterNN/ and bundles project files plus the required
data files from data/ into content/playground/chapterNN.zip.

Usage:
------
python data-raw/build_playground.py
"""

from pathlib import Path
import zipfile
import shutil
import tempfile

ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = ROOT / "playground-src"
OUT_ROOT = ROOT / "content" / "playground"
DATA_DIR = ROOT / "data"


def build_playground():
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    chapters = sorted([p for p in SRC_ROOT.iterdir() if p.is_dir() and p.name.startswith("chapter")])
    if not chapters:
        print("No chapter directories found in playground-src.")
        return

    print(f"Building playground zips for {len(chapters)} chapters...")

    for chapter_path in chapters:
        chapter = chapter_path.name

        with tempfile.TemporaryDirectory() as temp_dir:
            staging_dir = Path(temp_dir) / chapter
            staging_dir.mkdir(parents=True, exist_ok=True)

            # 1. Copy project files (everything except files.txt)
            project_files_count = 0
            for item in chapter_path.iterdir():
                if item.name == "files.txt":
                    continue
                dest = staging_dir / item.name
                if item.is_dir():
                    shutil.copytree(item, dest)
                else:
                    shutil.copy2(item, dest)
                project_files_count += 1

            # 2. Copy requested data files
            files_txt = chapter_path / "files.txt"
            data_files_count = 0
            if files_txt.exists():
                lines = [line.strip() for line in files_txt.read_text(encoding="utf-8").splitlines()]
                lines = [line for line in lines if line and not line.startswith("#")]

                for line in lines:
                    if "->" in line:
                        src_name, target_folder = [p.strip() for p in line.split("->", 1)]
                    else:
                        src_name, target_folder = line, "."

                    src_file = (DATA_DIR / src_name).resolve()
                    if not src_file.exists():
                        raise FileNotFoundError(f"Required data file '{src_name}' not found at {src_file} for {chapter}")

                    dest_folder = staging_dir / target_folder
                    dest_folder.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, dest_folder / Path(src_name).name)
                    data_files_count += 1

            # 3. Create zip file
            zip_dest = OUT_ROOT / f"{chapter}.zip"
            if zip_dest.exists():
                zip_dest.unlink()

            with zipfile.ZipFile(zip_dest, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
                for file_path in staging_dir.rglob("*"):
                    if file_path.is_file():
                        arcname = file_path.relative_to(Path(temp_dir))
                        zipf.write(file_path, arcname)

            print(f"  {chapter}: {project_files_count} project files + {data_files_count} data files -> {zip_dest.name}")

    print("Playground zips built successfully.")


if __name__ == "__main__":
    build_playground()
