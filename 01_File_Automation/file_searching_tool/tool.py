from pathlib import Path


class FileSearchingTool:
    def __init__(self):
        self.root = Path(__file__).resolve().parent

    def search_files_by_filename_non_recursively(self, file_name: str, folder=None):
        root = Path(folder) if folder else self.root
        results = []

        for file in root.glob(file_name):
            if file.is_file():
                results.append(str(file))
        if not results:
            return f"No files are found with name '{file_name}'"
        return f"Fetched Files are\n{",\n".join(results)}"

    def search_files_by_extension_non_recursively(self, pattern: str, folder=None):
        root = Path(folder) if folder else self.root

        results = []
        for file in root.glob("*." + pattern):
            if file.is_file():
                results.append(str(file))

        if not results:
            return f"No files are found with name '{pattern}'"
        return f"Fetched Files are\n{",\n".join(results)}"

    def search_files_by_filename_recursively(self, file_name: str, folder=None):
        root = Path(folder) if folder else self.root
        results = []
        for file in root.rglob(file_name):
            if file.is_file():
                results.append(str(file))
        if not results:
            return f"No files are found with name '{file_name}'"
        return f"Fetched Files are\n{",\n".join(results)}"

    def search_files_by_extension_recursively(self, pattern: str, folder=None):
        root = Path(folder) if folder else self.root

        results = []
        for file in root.rglob("*." + pattern):
            if file.is_file():
                results.append(str(file))

        if not results:
            return f"No files are found with name '{pattern}'"
        return f"Fetched Files are\n{",\n".join(results)}"


tool = FileSearchingTool()

print(tool.search_files_by_filename_recursively("anil.py"))
