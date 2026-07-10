from docx import Document


def load_docx(path: str) -> str:
    document = Document(path)

    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )