import pathlib
from loguru import logger
import fitz


def read_pdf_text(pdf_path: pathlib.Path, max_pages: int = 250) -> str:
    doc = fitz.open(pdf_path)
    texts = []
    for i, page in enumerate(doc):
        if i >= max_pages:
            break
        texts.append(page.get_text("text"))
    logger.info("Read {} pages of PDF", len(texts))
    return "\n\n".join(texts) 