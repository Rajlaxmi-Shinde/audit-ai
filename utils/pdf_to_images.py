import fitz
from pathlib import Path


def pdf_to_images(pdf_path: str, output_dir: str):
    """
    Convert every page of a PDF into a PNG image.
    """

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    pdf = fitz.open(pdf_path)

    for page_no in range(len(pdf)):
        page = pdf.load_page(page_no)

        pix = page.get_pixmap(dpi=300)

        image_path = Path(output_dir) / f"page_{page_no+1}.png"

        pix.save(str(image_path))

    pdf.close()