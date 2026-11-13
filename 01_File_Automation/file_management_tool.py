from pathlib import Path
import shutil
from datetime import datetime
import pymupdf
from docx import Document
import json
import csv
import tinycss2
import ast
from tree_sitter_language_pack import get_parser


class FileAutomationTool:
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

    def _resolve_folder(self, folder):
        """Helper to resolve relative, absolute, or None folder paths safely against self.root."""
        if not folder:
            return self.root
        folder_path = Path(folder)
        return folder_path if folder_path.is_absolute() else self.root / folder_path

    def _resolve_path(self, path_str):
        """Helper to resolve relative, absolute, or None paths safely against self.root."""
        if not path_str:
            return self.root
        p = Path(path_str)
        return p if p.is_absolute() else self.root / p

    def validate_code(self, file_path, content):

        extension = file_path.suffix.lower()

        try:

            # Python
            if extension == ".py":
                ast.parse(content)
                return True, "Code validation successful"

            # JavaScript, JSX, TypeScript, TSX, HTML
            elif extension in {".js", ".jsx", ".ts", ".tsx", ".html"}:

                language_map = {
                    ".js": "javascript",
                    ".jsx": "javascript",
                    ".ts": "typescript",
                    ".tsx": "tsx",
                    ".html": "html",
                }

                parser = get_parser(language_map[extension])
                tree = parser.parse(content.encode("utf-8"))

                if tree.root_node.has_error:
                    return False, "Syntax errors detected"

            # CSS
            elif extension == ".css":

                rules = tinycss2.parse_stylesheet(
                    content, skip_whitespace=True, skip_comments=True
                )

                errors = [rule for rule in rules if rule.type == "error"]

                if errors:
                    return False, str(errors)

            else:
                return True, "No validator configured"

            return True, "Code validation successful"

        except SyntaxError as e:
            return False, str(e)

        except Exception as e:
            return False, str(e)

    def create_files(self, *filenames, folder=None):
        if folder:
            folder_path = Path(folder)
            folder = (
                folder_path if folder_path.is_absolute() else self.root / folder_path
            )
        else:
            folder = self.root

        folder.mkdir(exist_ok=True, parents=True)
        count = 0
        for file in filenames:
            file_path = folder / file
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch(exist_ok=True)
            count += 1
        return f"Successfully created {count} files:\n" + ",\n".join(filenames)

    def create_folders(self, *dir_names, parent=None):
        if parent:
            parent_path = Path(parent)
            parent = (
                parent_path if parent_path.is_absolute() else self.root / parent_path
            )
        else:
            parent = self.root

        parent.mkdir(exist_ok=True, parents=True)

        count = 0
        for dir_name in dir_names:
            folder_path = parent / dir_name
            folder_path.mkdir(parents=True, exist_ok=True)
            count += 1

        return f"Successfully created {count} folders:\n" + ",\n".join(dir_names)

    def delete_file(self, file_name, folder=None):
        if folder:
            folder_path = Path(folder)
            target_root = (
                folder_path if folder_path.is_absolute() else self.root / folder_path
            )
        else:
            target_root = self.root

        file_path = target_root / file_name

        if not file_path.is_file():
            return "File not found"

        allowed = self.request_permission(operation="FILE DELETION", path=file_name)

        if isinstance(allowed, bool):
            if allowed is not True:
                return "Deletion cancelled by user"
        else:
            return f"{allowed}, File Deletion Failed"

        file_path.unlink()
        return f"File successfully deleted: {file_name}"

    def delete_folder(self, folder_name, parent=None):
        if parent:
            parent_path = Path(parent)
            target_root = (
                parent_path if parent_path.is_absolute() else self.root / parent_path
            )
        else:
            target_root = self.root

        folder_path = target_root / folder_name

        if not folder_path.is_dir():
            return "Folder not found"

        allowed = self.request_permission(operation="FOLDER DELETION", path=folder_name)

        if allowed is not True:
            return "Deletion cancelled by user"

        shutil.rmtree(folder_path)
        return f"Successfully deleted folder: {folder_name}"

    def create_project_structure(self, structure: dict):
        project_name = structure.get("project_name")
        parent = self.root / project_name if project_name else self.root

        parent.mkdir(exist_ok=True, parents=True)

        for folder, files in structure["folders"].items():
            folder_path = parent / folder
            folder_path.mkdir(exist_ok=True, parents=True)
            self.create_files(*files, folder=folder_path)

        return "Project Structure Created Successfully"

    def _resolve_folder(self, folder):
        """Helper to resolve relative, absolute, or None folder paths safely against self.root."""
        if not folder:
            return self.root
        folder_path = Path(folder)
        return folder_path if folder_path.is_absolute() else self.root / folder_path

    def search_files_by_filename_non_recursively(self, file_name: str, folder=None):
        root = self._resolve_folder(folder)
        results = []

        for file in root.glob(file_name):
            if file.is_file():
                results.append(str(file))

        if not results:
            return f"No files are found with name '{file_name}'"
        return "Fetched Files are\n" + ",\n".join(results)

    def search_files_by_extension_non_recursively(self, pattern: str, folder=None):
        root = self._resolve_folder(folder)
        clean_pattern = pattern.lstrip(".")
        results = []

        for file in root.glob(f"*.{clean_pattern}"):
            if file.is_file():
                results.append(str(file))

        if not results:
            return f"No files are found with extension '{pattern}'"
        return "Fetched Files are\n" + ",\n".join(results)

    def search_files_by_filename_recursively(self, file_name: str, folder=None):
        root = self._resolve_folder(folder)
        results = []

        for file in root.rglob(file_name):
            if file.is_file():
                results.append(str(file))

        if not results:
            return f"No files are found with name '{file_name}'"
        return "Fetched Files are\n" + ",\n".join(results)

    def search_files_by_extension_recursively(self, pattern: str, folder=None):
        root = self._resolve_folder(folder)
        clean_pattern = pattern.lstrip(".")
        results = []

        for file in root.rglob(f"*.{clean_pattern}"):
            if file.is_file():
                results.append(str(file))

        if not results:
            return f"No files are found with extension '{pattern}'"
        return "Fetched Files are\n" + ",\n".join(results)

    def list_files_by_filename_non_recursively(self, file_name: str, folder=None):
        root = self._resolve_folder(folder)
        results = []

        for file in root.glob(file_name):
            if file.is_file():
                results.append(str(file))
        if not results:
            return f"No files are found with name '{file_name}'"
        return "Fetched Files are\n" + ",\n".join(results)

    def list_files_by_extension_non_recursively(self, pattern: str, folder=None):
        root = self._resolve_folder(folder)
        clean_pattern = pattern.lstrip(".")
        results = []

        for file in root.glob(f"*.{clean_pattern}"):
            if file.is_file():
                results.append(str(file))

        if not results:
            return f"No files are found with name '{pattern}'"
        return "Fetched Files are\n" + ",\n".join(results)

    def list_files_by_filename_recursively(self, file_name: str, folder=None):
        root = self._resolve_folder(folder)
        results = []
        for file in root.rglob(file_name):
            if file.is_file():
                results.append(str(file))
        if not results:
            return f"No files are found with name '{file_name}'"
        return "Fetched Files are\n" + ",\n".join(results)

    def list_files_by_extension_recursively(self, pattern: str, folder=None):
        root = self._resolve_folder(folder)
        clean_pattern = pattern.lstrip(".")
        results = []

        for file in root.rglob(f"*.{clean_pattern}"):
            if file.is_file():
                results.append(str(file))

        if not results:
            return f"No files are found with name '{pattern}'"
        return "Fetched Files are\n" + ",\n".join(results)

    def get_directory_tree(self, folder=None, max_depth=None):
        root = self._resolve_folder(folder)
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

    def copy_files(self, *files, source=None, destination=None):
        if not destination:
            return {"error": "Destination is not specified."}

        src_root = self._resolve_path(source)
        dst_root = self._resolve_path(destination)
        dst_root.mkdir(parents=True, exist_ok=True)

        copied = []
        failed = []

        for file_item in files:
            src = src_root / file_item
            dst = dst_root / file_item

            if not src.is_file():
                failed.append(
                    {"file": str(file_item), "reason": "Source file does not exist"}
                )
                continue

            if dst.exists():
                failed.append(
                    {
                        "file": str(file_item),
                        "reason": "Destination file already exists",
                    }
                )
                continue

            dst.parent.mkdir(parents=True, exist_ok=True)

            try:
                shutil.copy2(src, dst)
                copied.append(str(dst))
            except Exception as e:
                failed.append({"file": str(file_item), "reason": str(e)})

        return {
            "success": f"copied {len(copied)} files",
            "copied_files": copied,
            "failed_files": failed,
        }

    def copy_dirs(self, *dirs, source=None, destination=None):
        if not destination:
            return {"error": "Destination is not specified."}

        src_root = self._resolve_path(source)
        dst_root = self._resolve_path(destination)
        dst_root.mkdir(parents=True, exist_ok=True)

        copied = []
        failed = []

        for dir_item in dirs:
            src = src_root / dir_item
            dst = dst_root / dir_item

            if not src.is_dir():
                failed.append(
                    {"dir": str(dir_item), "reason": "Source directory does not exist"}
                )
                continue

            if dst.exists():
                failed.append(
                    {"dir": str(dir_item), "reason": "Destination already exists"}
                )
                continue

            dst.parent.mkdir(parents=True, exist_ok=True)

            try:
                shutil.copytree(src, dst)
                copied.append(str(dst))
            except Exception as e:
                failed.append({"dir": str(dir_item), "reason": str(e)})

        return {
            "success": f"copied {len(copied)} directories",
            "copied_dirs": copied,
            "failed_dirs": failed,
        }

    def copy_all_files(self, source=None, destination=None):
        src_root = self._resolve_path(source)
        dst_root = self._resolve_path(destination)
        dst_root.mkdir(parents=True, exist_ok=True)

        copied_files = []
        skipped_files = []

        for item in src_root.iterdir():
            if item.is_file():
                target_path = dst_root / item.name

                if target_path.exists():
                    skipped_files.append(item.name)
                    continue

                shutil.copy2(item, target_path)
                copied_files.append(item.name)

        if not copied_files and not skipped_files:
            return f"No files found to copy in '{src_root}'."

        summary = f"Copied {len(copied_files)} file(s) to '{dst_root}'."
        if skipped_files:
            summary += (
                f" Skipped {len(skipped_files)} file(s) because they already exist."
            )

        return summary

    def copy_all_dirs(self, source=None, destination=None):
        src_root = self._resolve_path(source)
        dst_root = self._resolve_path(destination)
        dst_root.mkdir(parents=True, exist_ok=True)
        count = 0

        for sub_dir in src_root.iterdir():
            if sub_dir.is_dir():
                dst = dst_root / sub_dir.name
                if dst.exists():
                    continue
                shutil.copytree(sub_dir, dst)
                count += 1
        return f"Successfully copied {count} directories"

    def copy_directory(self, source=None, destination=None):
        src_root = self._resolve_path(source)
        dst_root = self._resolve_path(destination)

        if not src_root.is_dir():
            return f"source directory '{src_root}' not found"

        if dst_root == src_root or src_root in dst_root.parents:
            return "Cannot copy a directory into itself or its subdirectory"

        shutil.copytree(src_root, dst_root, dirs_exist_ok=True)

        return {
            "success": True,
            "source": str(src_root),
            "destination": str(dst_root),
            "message": "Directory copied successfully",
        }

    def rename_file(self, file_name, rename, source=None):
        root = self._resolve_path(source)
        file = root / file_name

        if file.is_file():
            target = file.with_name(rename)
            if target.exists():
                return f"A file named '{rename}' already exists."
            file.rename(target)
            return "File Renamed Successfully"

        return f"File '{file_name}' Not Found"

    def rename_directory(self, dir_name, rename, source=None):
        root = self._resolve_path(source)
        directory = root / dir_name

        if directory.is_dir():
            target = directory.with_name(rename)
            if target.exists():
                return f"A directory named '{rename}' already exists."
            directory.rename(target)
            return "Folder Renamed Successfully"

        return f"Folder '{dir_name}' Not Found"

    def move_file(self, file_name, source=None, destination=None):
        if not destination:
            return "Destination is not specified, Please tell the destination address"

        file_source = self._resolve_path(source)
        file_destination = self._resolve_path(destination)
        file_destination.mkdir(exist_ok=True, parents=True)

        file = file_source / file_name

        if file.is_file():
            dst_file = file_destination / file_name
            if dst_file.exists():
                return f"A file named '{file_name}' already exists in '{destination}'."
            shutil.move(str(file), str(dst_file))
            return f"Successfully '{file_name}' Moved to directory '{destination}'"
        return f"File '{file_name}' not found."

    def move_directory(self, directory_name, source=None, destination=None):
        if not destination:
            return "Destination is not specified, Please tell the destination address"

        directory_source = self._resolve_path(source)
        directory_destination = self._resolve_path(destination)
        directory_destination.mkdir(exist_ok=True, parents=True)

        directory = directory_source / directory_name

        if directory.is_dir():
            dst_directory = directory_destination / directory_name
            if dst_directory.exists():
                return f"A directory named '{directory_name}' already exists in '{destination}'."
            shutil.move(str(directory), str(dst_directory))
            return f"Successfully '{directory_name}' Moved to directory '{destination}'"
        return f"Directory '{directory_name}' not found."

    def get_file_metadata(self, file_name, folder=None):
        root = self._resolve_path(folder)
        file = root / file_name

        if not file.is_file():
            return "File Doesn't Exist"

        stat_info = file.stat()

        return {
            "file_name": file_name,
            "file_size": stat_info.st_size,
            "extension": file.suffix,
            "metadata": {
                "created_at": datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
            },
            "path": str(file),
        }

    def read_pdf(self, file):
        doc = pymupdf.open(str(file))
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()

    def read_docx(self, file):
        doc = Document(str(file))
        text = "\n".join(
            paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()
        )
        return text.strip()

    def read_json(self, file):
        with file.open("r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        return data

    def read_csv(self, file):
        with file.open("r", encoding="utf-8", newline="") as csv_file:
            data = list(csv.DictReader(csv_file))
        return data

    def read_file(self, file_name, source=None):
        src_root = self._resolve_path(source)
        file = src_root / file_name

        if not file.is_file():
            raise FileNotFoundError(f"File '{file_name}' not found")

        extension = file.suffix.lower()
        content = None

        if extension == ".pdf":
            content = self.read_pdf(file)
        elif extension == ".docx":
            content = self.read_docx(file)
        elif extension == ".json":
            content = self.read_json(file)
        elif extension == ".csv":
            content = self.read_csv(file)
        else:
            with file.open("r", encoding="utf-8") as reader:
                content = reader.read()

        if content is None or (isinstance(content, str) and not content.strip()):
            return f"No text found in '{file_name}'. It's empty."

        return content

    def delete_content(self, file_name, start_line, end_line, source=None):

        file_path = self._resolve_path(source) / file_name

        if not file_path.is_file():
            return "File not found"

        try:
            if self.request_permission("editing a file", file_path) != True:
                return f"File editing request cancelled"

            lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)

            # Line numbers are 1-based and inclusive
            if not (1 <= start_line <= end_line <= len(lines)):
                return "Invalid line range"

            updated_lines = lines[: start_line - 1] + lines[end_line:]

            updated_content = "".join(updated_lines)

            if file_path.suffix.lower() == ".py":
                is_valid, message = self.validate_code(file_path, updated_content)

                if not is_valid:
                    return f"Modification rejected: {message}"

            file_path.write_text(updated_content, encoding="utf-8")

            return f"Deleted lines {start_line} to {end_line}"

        except SyntaxError as e:
            return f"Python syntax error: {e}"

        except Exception as e:
            return f"Deletion failed: {e}"

    def replace_content(self, file_name, old_content, new_content, source=None):

        file_path = self._resolve_path(source) / file_name

        if not file_path.is_file():
            return "File not found"

        try:
            content = file_path.read_text(encoding="utf-8")

            # Ensure the old content exists exactly once
            count = content.count(old_content)

            if count == 0:
                return "Old content not found"

            if count > 1:
                return f"Found {count} matches. Edit cancelled to avoid ambiguity."

            updated_content = content.replace(old_content, new_content, 1)

            is_valid, message = self.validate_code(file_path, updated_content)

            if not is_valid:
                return f"Modification rejected: {message}"

            file_path.write_text(updated_content, encoding="utf-8")

            return "Content replaced successfully"

        except SyntaxError as e:
            return f"Python syntax error: {e}"

        except Exception as e:
            return f"Edit failed: {e}"

    def write_file(self, file_name, content, source=None, mode="w"):
        file_path = self._resolve_path(source) / file_name

        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)

        extension = file_path.suffix.lower()

        try:
            # 1. Text-based files
            text_extensions = {
                ".txt",
                ".py",
                ".js",
                ".jsx",
                ".html",
                ".css",
                ".md",
                ".xml",
                ".sql",
                ".yaml",
                ".yml",
                ".ts",
                ".tsx",
                ".java",
                ".cpp",
                ".c",
            }

            if extension in text_extensions:
                if mode not in {"w", "a"}:
                    return "Text files support only 'w' or 'a' modes."

                content_str = str(content)

                # Validate full resulting file content (important when appending)
                if mode == "a" and file_path.exists():
                    full_content = file_path.read_text(encoding="utf-8") + content_str
                else:
                    full_content = content_str

                is_valid, message = self.validate_code(file_path, full_content)
                if not is_valid:
                    return f"Modification rejected: {message}"

                with file_path.open(mode, encoding="utf-8") as file:
                    file.write(content_str)

            # 2. JSON files
            elif extension == ".json":
                if mode != "w":
                    return "JSON supports overwrite mode only."

                # If content is passed as a JSON string, parse it first to avoid double-encoding
                if isinstance(content, str):
                    try:
                        content = json.loads(content)
                    except json.JSONDecodeError as e:
                        return f"Invalid JSON string: {str(e)}"

                with file_path.open("w", encoding="utf-8") as file:
                    json.dump(content, file, indent=4, ensure_ascii=False)

            # 3. CSV files
            elif extension == ".csv":
                if not isinstance(content, list):
                    return "CSV content must be a list."
                if not content:
                    return "CSV content cannot be empty."
                if not all(isinstance(row, dict) for row in content):
                    return "CSV content must contain a list of dictionaries."
                if mode not in {"w", "a"}:
                    return "CSV supports only 'w' or 'a' modes."

                write_header = (
                    (mode == "w")
                    or (not file_path.exists())
                    or (file_path.stat().st_size == 0)
                )

                with file_path.open(mode, encoding="utf-8", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=content[0].keys())
                    if write_header:
                        writer.writeheader()
                    writer.writerows(content)

            # 4. DOCX files
            elif extension == ".docx":
                if mode not in {"w", "a"}:
                    return "DOCX supports only 'w' or 'a' modes."

                if mode == "a" and file_path.exists():
                    doc = Document(str(file_path))
                else:
                    doc = Document()

                if isinstance(content, list):
                    for paragraph in content:
                        doc.add_paragraph(str(paragraph))
                else:
                    for line in str(content).splitlines():
                        doc.add_paragraph(line)

                doc.save(str(file_path))

            # 5. PDF files
            elif extension == ".pdf":
                if mode != "w":
                    return "PDF currently supports overwrite mode only."

                doc = pymupdf.open()
                page = doc.new_page()
                rect = page.rect + (50, 50, -50, -50)

                text = str(content)
                result = page.insert_textbox(rect, text, fontsize=11, fontname="helv")

                if result < 0:
                    doc.close()
                    return "Content is too large for one PDF page."

                doc.save(str(file_path))
                doc.close()

            else:
                return f"Unsupported file format: {extension}"

            return f"Successfully wrote content to: {file_path}"

        except Exception as e:
            return f"File writing failed: {str(e)}"

    def get_file_path(self, file_name):
        fetched_files = {}
        for file in Path("C:/Users/rolex/OneDrive/Desktop").rglob(file_name):
            if file.is_file():
                return file

    def get_folder_path(self, dir_name):
        for dir in Path("C:/Users/rolex/OneDrive/Desktop").rglob(dir_name):
            if dir.is_dir():
                return dir

    def zip_folder(self, folder_name, output_zip_path=None):

        folder_path = (
            Path(folder_name) if folder_name else self.get_folder_path(folder_name)
        )

        if not folder_path.is_dir():
            return f"Invalid folder path given"

        try:
            output_zip_path = Path(output_zip_path) if output_zip_path else self.root

            shutil.make_archive(
                base_name=str(output_zip_path.with_suffix("")),
                format="zip",
                root_dir=str(folder_path),
            )
            return f"Zip creation successfull for the file {folder_name}"
        except Exception as e:
            return f"ZIP Creation Failed due to, {str(e)} "


if __name__ == "__main__":
    tool = FileAutomationTool()

    structure = {
        "project_name": "project",
        "folders": {
            "backend": ["main.py", "model.py", "database.py"],
            "frontend": ["index.html"],
        },
    }

    print(tool.zip_folder("01_File_Automation"))
