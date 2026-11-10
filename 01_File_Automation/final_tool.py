from pathlib import Path
import shutil
from datetime import datetime


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

        project_folder = structure.get("project_name")

        root = (self.root / project_folder) if project_folder else self.root
        root.mkdir(exist_ok=True, parents=True)

        for folder, files in structure["folders"].items():
            dir_path = root / folder
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
        if count == 0:
            return f"No files are found with name '{file_name}'"
        return f"Succesfully Deleted {count} files"

    def delete_dir(self, dir_name, folder=None):
        root = Path(folder) if folder else self.root

        count = 0
        for dir in root.glob(dir_name):
            if dir.is_dir():
                shutil.rmtree(dir)
                count += 1
        if count == 0:
            return f"No folders are found with name '{dir_name}'"
        return f"Succesfully Deleted folder '{dir_name}'"

    def list_files_non_recursively(self, file_name, folder=None):
        root = Path(folder) if folder else self.root

        results = []
        for file in root.glob(file_name):
            if file.is_file():
                results.append(str(file))
        if not results:
            return f"No files are found with name '{file_name}' "
        return f"succesfully fetched {len(results)} ,{", ".join(results)}"

    def list_files_recursively(self, file_name, folder=None):
        root = Path(folder) if folder else self.root

        results = []
        for file in root.rglob(file_name):
            if file.is_file():
                results.append(str(file))
        if not results:
            return f"No files are found with name '{file_name}' "
        return f"succesfully fetched {len(results)} files,{", ".join(results)}"

    def list_dirs_non_recursively(self, dir_name, folder=None):
        root = Path(folder) if folder else self.root

        results = []
        for dir in root.glob(dir_name):
            if dir.is_dir():
                results.append(str(dir))
        if not results:
            return f"No folders are found with name '{dir_name}' "
        return f"succesfully fetched {len(results)} folders,{", ".join(results)}"

    def get_file_info(self, file_name, folder=None):
        root = Path(folder) if folder else self.root
        file = root / file_name
        if file.is_file():
            stat_info = file.stat()
            return {
                "name": file_name,
                "size": stat_info.st_size,
                "path": str(file.resolve()),
                "metadata": {
                    "created": datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                    "extension": file.suffix,
                },
            }
        return f"No file is found with name '{file_name}'"

    def get_directory_tree(self, folder=None, max_depth=None):
        root = Path(folder) if folder else self.root
        if not root.is_dir():
            return f"Error: '{root}' is not a valid directory."

        lines = [f"{root.resolve().name}/"]

        def _build_tree(directory: Path, prefix: str = "", depth: int = 0):
            if max_depth is not None and depth >= max_depth:
                return

            try:
                # Sort directories first, then files alphabetically
                entries = sorted(
                    directory.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())
                )
            except PermissionError:
                lines.append(f"{prefix}└── [Permission Denied]")
                return

            total = len(entries)
            for index, path in enumerate(entries):
                is_last = index == total - 1
                connector = "└── " if is_last else "├── "

                # Append folder trailing slash for clarity
                display_name = f"{path.name}/" if path.is_dir() else path.name
                lines.append(f"{prefix}{connector}{display_name}")

                if path.is_dir():
                    extension = "    " if is_last else "│   "
                    _build_tree(path, prefix + extension, depth + 1)

        _build_tree(root)
        return "\n".join(lines)


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

print(file_tool.project_structure(structure))

# print(file_tool.search_files_by_filename("tool"))
# print(file_tool.search_files_by_extension("py", "01_File_Management_Automation_Tool"))

# print(file_tool.delete_file("demo.py", "01_File_Management_Automation_Tool"))
# print(file_tool.delete_dir("project"))

# print(
#     file_tool.list_files(
#         "4Sum.py",
#         r"C:\Users\rolex\OneDrive\Desktop\LeetCode\Two Pointers + Sliding Window",
#     )
# )

# print(file_tool.get_file_info("pathlib_lab.ipynb"))

print(file_tool.get_directory_tree("01_File_Management_Automation_Tool"))
