from pathlib import Path
from pypdf import PdfReader


def extract_text(filename: str, content: bytes) -> str:
    extension = Path(filename).suffix.lower()

    # TXT and Markdown
    if extension in {".txt", ".md"}:
        return content.decode("utf-8")

    # PDF
    if extension == ".pdf":
        path = "/tmp/document.pdf"

        with open(path, "wb") as file:
            file.write(content)

        reader = PdfReader(path)

        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

        return text

    raise ValueError(
        "Unsupported file type. Use PDF, TXT, or Markdown."
    )