import shutil
from pathlib import Path
import tomllib



DOWNLOADS_DIR = Path.home() / "Downloads"

with open(Path(__file__).parent / "config.toml", "rb") as f:
    config = tomllib.load(f)

CATEGORIES = config.get("categories", {})
DIRECTORY_TARGET = config.get("directory_target", "Folders")
IGNORE_EXTENSIONS = set(config.get("ignore_extensions", []))

PROTECTED = {DIRECTORY_TARGET} | set(CATEGORIES.keys())

DRY_RUN = config.get("dry_run", True)



def get_unique_path(target_path: Path) -> Path:
    """Handles name collisions for both files and directories."""
    if not target_path.exists():
        return target_path

    # For directories without an extension, suffix is empty and stem is the folder name
    stem = target_path.stem if target_path.suffix else target_path.name
    suffix = target_path.suffix if target_path.suffix else ""
    counter = 1

    while True:
        new_path = target_path.parent / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def categorise_item(item: Path) -> str:
    if item.is_dir() and item.suffix.lower() == ".app":
        return "Installers"
    
    # Generic directory
    if item.is_dir():
        return DIRECTORY_TARGET

    # File categorisation
    ext = item.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category

        
    return "Other"


def organise(dry_run: bool = True):
    if not DOWNLOADS_DIR.exists():
        print(f"Error: {DOWNLOADS_DIR} does not exist.")
        return

    moved_count = 0

    for item in DOWNLOADS_DIR.iterdir():
        # Skip hidden files
        if item.name.startswith("."):
            continue

        # Skip destination folders
        if item.is_dir() and item.name in PROTECTED:
            continue

        # Skip downloads
        if item.suffix.lower() in IGNORE_EXTENSIONS:
            continue

        category = categorise_item(item)
        target_dir = DOWNLOADS_DIR / category
        destination = target_dir / item.name

        # Handle dry runs
        if dry_run:
            item_type = "Folder" if item.is_dir() and item.suffix.lower() != ".app" else "File"
            print(f"[Dry Run] Would move {item_type}: {item.name} -> {category}/")
            moved_count += 1

            # Skip the actual move operation in dry run mode
            continue

        target_dir.mkdir(exist_ok=True)
        final_destination = get_unique_path(destination)

        try:
            shutil.move(str(item), str(final_destination))
            print(f"Moved: {item.name} -> {category}/{final_destination.name}")
            moved_count += 1
        except Exception as e:
            print(f"Failed to move {item.name}: {e}")

    print(f"\nFinished. Total items processed: {moved_count}")


if __name__ == "__main__":
    organise(dry_run=DRY_RUN)