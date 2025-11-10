import re

_SENT_SPLIT = re.compile(r'(?<=[.!?])\s+')


def split_text_for_llm(text: str, max_chars: int = 3000) -> list[str]:
    """Split text into chunks near sentence boundaries to fit model limits."""
    text = text.strip()
    if len(text) <= max_chars:
        return [text]
    parts = _SENT_SPLIT.split(text)
    chunks, buf = [], ''

    for p in parts:
        if len(buf) + len(p) + 1 <= max_chars:
            buf = (buf + ' ' + p).strip()
        else:
            if buf:
                chunks.append(buf)
            if len(p) <= max_chars:
                buf = p
            else:
                for i in range(0, len(p), max_chars):
                    chunks.append(p[i : i + max_chars])
                buf = ''
    if buf:
        chunks.append(buf)
    return chunks
