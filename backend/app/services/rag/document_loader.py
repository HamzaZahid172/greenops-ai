from io import BytesIO
from pathlib import Path

from pypdf import PdfReader

from app.core.config import settings


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".yaml",
    ".yml",
    ".json",
    ".pdf",
}


def load_document_text(
    filename: str,
    content: bytes,
) -> str:

    extension = (
        Path(filename)
        .suffix
        .lower()
    )

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported document type: "
            f"{extension}"
        )

    max_bytes = (
        settings.rag_max_file_size_mb
        * 1024
        * 1024
    )

    if len(content) > max_bytes:
        raise ValueError(
            "Document exceeds maximum "
            "file size."
        )

    if extension == ".pdf":

        reader = PdfReader(
            BytesIO(content)
        )

        pages = [
            page.extract_text() or ""
            for page in reader.pages
        ]

        text = "\n\n".join(pages)

    else:

        try:
            text = content.decode(
                "utf-8"
            )

        except UnicodeDecodeError as exc:
            raise ValueError(
                "Document must be UTF-8 encoded."
            ) from exc

    text = text.strip()

    if not text:
        raise ValueError(
            "Document contains no readable text."
        )

    return text