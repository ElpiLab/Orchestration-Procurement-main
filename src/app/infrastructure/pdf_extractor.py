from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError


def extract_text_from_pdf(content: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(content))
        text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    except (PdfReadError, OSError, ValueError) as exc:
        raise ValueError("The PDF could not be read") from exc
    if not text:
        raise ValueError("The PDF contains no extractable text")
    return text
