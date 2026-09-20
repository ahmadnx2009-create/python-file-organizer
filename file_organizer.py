from pathlib import Path
import shutil
# Folder where the files are located
SOURCE_FOLDER = Path.home() / "Downloads"
# File categories
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Python": [".py"],
    "Archives": [".zip", ".rar", ".7z"],
}
def get_category(extension):
    """Return the category for a file extension."""
    extension = extension.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"
def get_unique_destination(destination):
    """Prevent overwriting an existing file."""
    if not destination.exists():
        return destination
    counter = 1
    while True:
        new_name = f"{destination.stem}_{counter}{destination.suffix}"
        new_destination = destination.parent / new_name
        if not new_destination.exists():
            return new_destination
        counter += 1
def organize_files():
    if not SOURCE_FOLDER.exists():
        print(f"Folder not found: {SOURCE_FOLDER}")
        return
    moved_count = 0
    for file in SOURCE_FOLDER.iterdir():
        # Ignore folders
        if not file.is_file():
            continue
        # Ignore this script
        if file.name == Path(__file__).name:
            continue
        category = get_category(file.suffix)
        destination_folder = SOURCE_FOLDER / category
        destination_folder.mkdir(exist_ok=True)
        destination = destination_folder / file.name
        destination = get_unique_destination(destination)
        try:
            shutil.move(str(file), str(destination))
            print(f"Moved: {file.name} -> {category}")
            moved_count += 1
        except PermissionError:
            print(f"Permission denied: {file.name}")
        except OSError as error:
            print(f"Could not move {file.name}: {error}")
    print()
    print(f"Finished. Files organized: {moved_count}")
if __name__ == "__main__":
    organize_files()
