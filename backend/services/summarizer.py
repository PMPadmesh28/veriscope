import re
def summarize_text(text, max_chars=240):
    cleaned=re.sub(r"\s+"," ",text or "").strip()
    if not cleaned:return "No text available to summarize."
    # Lightweight extractive prototype: keep the first 1–2 sentences.
    sentences=re.split(r"(?<=[.!?])\s+",cleaned)
    summary=" ".join(sentences[:2]).strip()
    if len(summary)>max_chars: summary=summary[:max_chars].rsplit(" ",1)[0]+"…"
    return summary
