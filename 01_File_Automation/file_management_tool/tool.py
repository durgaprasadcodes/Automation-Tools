from pathlib import Path
import shutil


class FileManagementTool:
    def __init__(self):
        self.root = Path(__file__).resolve().parent

    def copy_files(self, *files, source=None, destination=None):
        if not destination:
            return {"error": "Destination is not specified."}

        source = Path(source) if source else self.root
        destination = Path(destination)
        destination.mkdir(parents=True, exist_ok=True)

        copied = []
        failed = []

        for file_item in files:
            src = source / file_item
            dst = destination / file_item

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

        source = Path(source) if source else self.root
        destination = Path(destination)
        destination.mkdir(parents=True, exist_ok=True)

        copied = []
        failed = []

        for dir_item in dirs:
            src = source / dir_item
            dst = destination / dir_item

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

        source = Path(source) if source else self.root
        destination = Path(destination) if destination else self.root
        destination.mkdir(parents=True, exist_ok=True)

        copied_files = []
        skipped_files = []

        for item in source.iterdir():
            if item.is_file():
                target_path = destination / item.name

                if target_path.exists():
                    skipped_files.append(item.name)
                    continue

                shutil.copy2(item, target_path)
                copied_files.append(item.name)

        if not copied_files and not skipped_files:
            return f"No files found to copy in '{source}'."

        summary = f"Copied {len(copied_files)} file(s) to '{destination}'."
        if skipped_files:
            summary += (
                f" Skipped {len(skipped_files)} file(s) because they already exist."
            )

        return summary

    def copy_all_dirs(self, source=None, destination=None):

        source = Path(source) if source else self.root
        destination = Path(destination) if destination else self.root
        destination.mkdir(parents=True, exist_ok=True)
        count = 0
        for dir in source.iterdir():
            if dir.is_dir():
                src = dir
                dst = destination / dir.name
                if dst.exists():
                    continue
                shutil.copy2(src, dst)
                count += 1
        return f"Successfully copied {count} dirs"

    def copy_directory(self, source=None, destination=None):

        source = Path(source) if source else self.root
        destination = Path(destination) if destination else self.root

        if not source.is_dir():
            return f"source directory '{source}' not found"

        if destination == source or source in destination.parents:
            return "Cannot copy a directory into itself or its subdirectory"

        shutil.copytree(source, destination, dirs_exist_ok=True)

        return {
            "success": True,
            "source": str(source),
            "destination": str(destination),
            "message": "Directory copied successfully",
        }

    def rename_file(self, file_name, rename, source=None):
        root = Path(source) if source else self.root

        file = root / file_name
        if file.is_file():
            # Keep the new file in the same directory
            target = file.with_name(rename)

            if target.exists():
                return f"A file named '{rename}' already exists."

            file.rename(target)
            return "File Renamed Successfully"

        return f"File '{file_name}' Not Found"

    def rename_directory(self, dir_name, rename, source=None):
        root = Path(source) if source else self.root

        dir = root / dir_name
        if dir.is_dir():
            # Keep the new dir in the same directory
            target = dir.with_name(rename)

            if target.exists():
                return f"A directory named '{rename}' already exists."

            dir.rename(target)
            return "Folder Renamed Successfully"

        return f"Folder '{dir_name}' Not Found"

    def move_file(self, file_name, source=None, destination=None):
        if not destination:
            return f"Destination is not specified, Please tell the destination address"

        file_source = Path(source) if source else self.root
        file_destination = Path(destination)
        file_destination.mkdir(exist_ok=True, parents=True)

        file = file_source / file_name

        if file.is_file():
            dst_file = file_destination / file_name
            if dst_file.exists():
                return f"A file named '{file_name}' already exists in '{destination}'."
            shutil.move(file, dst_file)
            return f"Succesfully '{file_name}' Moved to directory '{destination}'"
        return f"File '{file_name}' not found."

    def move_directory(self, directory_name, source=None, destination=None):
        if not destination:
            return f"Destination is not specified, Please tell the destination address"

        directory_source = Path(source) if source else self.root
        directory_destination = Path(destination)
        directory_destination.mkdir(exist_ok=True, parents=True)

        directory = directory_source / directory_name

        if directory.is_dir():
            dst_directory = directory_destination / directory_name
            if dst_directory.exists():
                return f"A directory named '{directory_name}' already exists in '{destination}'."
            shutil.move(directory, dst_directory)
            return f"Succesfully '{directory_name}' Moved to directory '{destination}'"
        return f"Directory '{directory_name}' not found."


tool = FileManagementTool()

print(tool.move_directory("agent", destination="backend"))
