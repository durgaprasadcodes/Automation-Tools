from pathlib import Path
import pymupdf
from docx import Document
import json
import csv


class ReadWriteAppendTool:
    def __init__(self):
        self.root = Path(__file__).resolve().parent

    def read_pdf(self, file):
        doc = pymupdf.open(file)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        return text.strip()

    def read_docx(self, file):
        doc = Document(file)
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
        source = Path(source) if source else self.root

        file = source / file_name

        if not file.is_file():
            raise FileNotFoundError(f"File '{file_name}' not found")

        extension = file.suffix.lower()

        if extension == ".pdf":
            text = self.read_pdf(file)
        elif extension == ".docx":
            text = self.read_docx(file)
        elif extension == ".json":
            text = self.read_json(file)
        elif extension == ".csv":
            text = self.read_csv(file)
        else:
            with file.open("r", encoding="utf-8") as reader:
                text = reader.read()

        return text if text else (f"No text found in '{file_name}'. It's empty.")


tool = ReadWriteAppendTool()

print(tool.read_file("readme.md"))
