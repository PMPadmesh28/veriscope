import re
def clean_text(text: str) -> str:
    text = text or ""
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"@\w+|#\w+", " ", text)
    text = re.sub(r"[^A-Za-z0-9\s.,!?'-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text
