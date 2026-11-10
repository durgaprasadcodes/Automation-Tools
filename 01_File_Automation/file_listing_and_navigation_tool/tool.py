from pathlib import Path


class FileListingAndNavigationTool:
    def __init__(self):
        self.root = Path(__file__).resolve().parent

    def list_files_by_filename_non_recursively(self, file_name: str, folder=None):
        root = Path(folder) if folder else self.root
        results = []

        for file in root.glob(file_name):
            if file.is_file():
                results.append(str(file))
        if not results:
            return f"No files are found with name '{file_name}'"
        return f"Fetched Files are\n{",\n".join(results)}"

    def list_files_by_extension_non_recursively(self, pattern: str, folder=None):
        root = Path(folder) if folder else self.root

        results = []
        for file in root.glob("*." + pattern):
            if file.is_file():
                results.append(str(file))

        if not results:
            return f"No files are found with name '{pattern}'"
        return f"Fetched Files are\n{",\n".join(results)}"

    def list_files_by_filename_recursively(self, file_name: str, folder=None):
        root = Path(folder) if folder else self.root
        results = []
        for file in root.rglob(file_name):
            if file.is_file():
                results.append(str(file))
        if not results:
            return f"No files are found with name '{file_name}'"
        return f"Fetched Files are\n{",\n".join(results)}"

    def list_files_by_extension_recursively(self, pattern: str, folder=None):
        root = Path(folder) if folder else self.root

        results = []
        for file in root.rglob("*." + pattern):
            if file.is_file():
                results.append(str(file))

        if not results:
            return f"No files are found with name '{pattern}'"
        return f"Fetched Files are\n{",\n".join(results)}"

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


tool = FileListingAndNavigationTool()

print(
    tool.get_directory_tree(folder=r"C:\Users\rolex\OneDrive\Desktop\LeetCode"),
)
