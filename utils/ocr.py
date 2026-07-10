from pathlib import Path
import easyocr


# Create the reader once (don't recreate it for every page)
reader = easyocr.Reader(["en"], gpu=False)


def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from a single image.
    """

    result = reader.readtext(
        image_path,
        detail=0,
        paragraph=True
    )

    return "\n".join(result)