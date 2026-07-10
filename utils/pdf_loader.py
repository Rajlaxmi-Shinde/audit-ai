import fitz  # PyMuPDF


def load_pdf(pdf_path: str) -> str:
    """
    Reads all pages from a PDF and returns the extracted text.
    """

    document = fitz.open(pdf_path)

    pages = []

    for page in document:
        text = page.get_text()
        pages.append(text)

    document.close()

    return "\n".join(pages)