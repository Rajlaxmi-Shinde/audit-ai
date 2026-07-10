import re

def extract_json(text: str):
    """
    Extracts JSON from LLM response even if wrapped in markdown.
    """

    if not text:
        return None

    # remove ```json and ```
    text = text.strip()

    # case 1: markdown fenced block
    if "```" in text:
        text = re.sub(r"```json", "", text)
        text = text.replace("```", "").strip()

    # case 2: extract first JSON object
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return text[start:end]
    except Exception:
        return text