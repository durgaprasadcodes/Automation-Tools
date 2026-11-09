from pathlib import Path

# file_path = Path(__file__)

# print(file_path)


class FileAutomationTool:

    def __init__(self, project_name=None):
        self.root = (
            Path(project_name) if project_name else Path(__file__).resolve().parent
        )

    def create_files(self, *files, folder=None):

        folder = Path(folder) if folder else self.root
        folder.mkdir(exist_ok=True, parents=True)

        for file in files:
            file_path = folder / file
            file_path.touch(exist_ok=True)

        return f"Files Successfully Created: {', '.join(files)}"

    def project_structure(self, structure: dict):

        self.root = Path(structure.get("project_name") or ".")
        self.root.mkdir(exist_ok=True, parents=True)

        for folder, files in structure["folders"].items():
            dir_path = self.root / folder
            dir_path.mkdir(exist_ok=True, parents=True)
            self.create_files(*files, folder=dir_path)

        return "Project Structure Created Successfully"

    def create_dirs(self, *dirs, root=None):
        root = Path(root) if root else self.root

        for directory in dirs:
            dir_path = root / directory
            dir_path.mkdir(exist_ok=True, parents=True)

        return f"Folders Successfully Created: {', '.join(dirs)}"

    def search_files_by_filename(self, file_name: str, folder=None):
        root = Path(folder) if folder else self.root

        results = []
        for file in root.rglob(file_name):
            if file.is_file():
                results.append(str(file))

        if not results:
            return f"No files are found with name '{file_name}'"
        return f"Fetched Files are {", ".join(results)}"

    def search_files_by_extension(self, pattern: str, folder=None):
        root = Path(folder) if folder else self.root

        results = []
        for file in root.rglob("*." + pattern):
            if file.is_file():
                results.append(str(file))

        if not results:
            return f"No files are found with name '{pattern}'"
        return f"Fetched Files are {", ".join(results)}"

    def delete_file(self, file_name, folder=None):
        root = Path(folder) if folder else self.root

        count = 0
        for file in root.glob(file_name):
            if file.is_file():
                file.unlink()
                count += 1
            else:
                print("yes")
        if count == 0:
            return f"No files are found with name '{file_name}'"
        return f"Succesfully Deleted {count} files"

    def delete_dir(self, dir_name, folder=None):
        root = Path(folder) if folder else self.root

        count = 0
        for dir in root.glob(dir_name):
            if dir.is_dir():
                dir.unlink()
                count += 1
        if count == 0:
            return f"No folders are found with name '{dir_name}'"
        return f"Succesfully Deleted folder '{dir_name}'"


# list_files(),list_dirs(),get_file_info(),file_exists(),get_directory_tree(),get_file_extension(),get_file_size()

# Testing

file_tool = FileAutomationTool()

structure = {
    "project_name": "project",
    "folders": {
        "backend": ["main.py", "model.py", "database.py"],
        "frontend": ["index.html"],
    },
}

# print(file_tool.project_structure(structure))

# print(file_tool.search_files_by_filename("tool"))
# print(file_tool.search_files_by_extension("py", "01_File_Management_Automation_Tool"))

# print(file_tool.delete_file("demo.py", "01_File_Management_Automation_Tool"))
