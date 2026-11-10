from pathlib import Path
from datetime import datetime


class MetaDataTool:
    def __init__(self):
        self.root = Path(__file__).resolve().parent

    def get_file_metadate(self, file_name, folder=None):
        root = Path(folder) if folder else self.root

        file = root / file_name
        if not file.is_file():
            return f"File Doesn't Exist"

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


tool = MetaDataTool()

print(tool.get_file_metadate("tool.py"))
