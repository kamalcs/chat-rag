from pathlib import Path

import fitz
from docx import Document


class DocumentLoader:

    def load(self, file_path: str) -> str:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        extension = path.suffix.lower()

        if extension == ".txt":
            return self._load_txt(path)

        if extension == ".pdf":
            return self._load_pdf(path)

        if extension == ".docx":
            return self._load_docx(path)

        raise ValueError(f"Unsupported file type: {extension}")

    def _load_txt(self, path: Path) -> str:

        return path.read_text(encoding="utf-8")

    def _load_pdf(self, path: Path) -> str:

        text = []

        with fitz.open(path) as document:

            for page in document:

                page_text = page.get_text()

                if page_text:
                    text.append(page_text)

        return "\n".join(text)

    def _load_docx(self, path: Path) -> str:

        document = Document(path)

        paragraphs = []

        for paragraph in document.paragraphs:

            if paragraph.text.strip():
                paragraphs.append(paragraph.text)

        return "\n".join(paragraphs)
