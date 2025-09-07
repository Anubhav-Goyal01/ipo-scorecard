import pathlib
from loguru import logger
import fitz
from typing import Optional


def read_pdf_text(pdf_path: pathlib.Path, max_pages: Optional[int] = None) -> str:
    doc = fitz.open(pdf_path)
    texts = []
    for i, page in enumerate(doc):
        if max_pages is not None and i >= max_pages:
            break
        texts.append(page.get_text("text"))
    logger.info("Read {} pages of PDF", len(texts))
    return "\n\n".join(texts) 