from pathlib import Path
import shutil

root = Path(__file__).resolve().parent


class FileCreationAndDeletion:
    def __init__(self):
        self.root = Path(__file__).resolve().parent

    def request_permission(self, operation, path):

        print("\n⚠️  Permission Required")
        print(f"Operation : {operation}")
        print(f"Target    : {path}")
        response = input("Do you want to continue? (yes/no): ").lower().strip()

        if response in {"yes", "y", "YES"}:
            return True
        elif response in {"no", "n", "NO"}:
            return False
        return "INVALID OPTION"

    def create_files(self, *filenames, folder=None):

        folder = Path(self.root / folder) if folder else self.root
        folder.mkdir(exist_ok=True, parents=True)
        count = 0
        for file in filenames:
            file_path = folder / file
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch(exist_ok=True)
            count += 1
        return f"succesfully created {count} files\n{",\n".join(filenames)}"

    def create_folders(self, *dir_names, parent=None):

        parent = Path(self.root / parent) if parent else self.root
        parent.mkdir(exist_ok=True, parents=True)

        count = 0
        for dir in dir_names:
            file_path = parent / dir
            file_path.mkdir(parents=True, exist_ok=True)
            count += 1

        return f"succesfully created {count} folders\n{",\n".join(dir_names)}"

    def delete_file(self, file_name, folder=None):

        root = Path(folder) if folder else self.root

        file_path = root / file_name

        if not file_path.is_file():
            return "File not found"

        allowed = self.request_permission(operation="FILE DELETION", path=file_name)

        if isinstance(allowed, bool):
            if not allowed:
                return "Deletion cancelled by user"
        else:
            return f"{allowed}, File Deletion Failed"

        file_path.unlink()

        return f"File successfully deleted: {file_name}"

    def delete_folder(self, folder_name, parent=None):
        global root
        root = Path(self.parent) if parent else self.root
        folder_path = root / folder_name

        if not folder_path.is_dir():
            return "Folder not found"

        allowed = self.request_permission(operation="FOLDER DELETION", path=folder_name)

        if not allowed:
            return "Deletion cancelled by user"

        shutil.rmtree(folder_path)

        return f"Successfully deleted: {folder_name}"

    def create_project_structure(self, structure: dict):

        parent = structure.get("project_name")
        parent = Path(self.root / parent) if parent else self.root

        parent.mkdir(exist_ok=True, parents=True)

        for folder, files in structure["folders"].items():
            folder_path = parent / folder
            folder_path.mkdir(exist_ok=True, parents=True)
            self.create_files(*files, folder=folder_path)

        return f"Project Structure Created Successfully"


structure = {
    "project_name": "project",
    "folders": {
        "backend": ["main.py", "model.py", "database.py"],
        "frontend": ["index.html"],
    },
}

tool = FileCreationAndDeletion()
print(tool.create_files("h1.txt", "h2.txt", "h2.txt", folder="HH"))
