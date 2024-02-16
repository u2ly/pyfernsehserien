import re


def normalize_text(text: str) -> str:
    text = text.replace("\\n", " ")

    return re.sub(r"\s+", " ", text).strip()
