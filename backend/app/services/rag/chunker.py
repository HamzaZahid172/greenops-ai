from app.core.config import settings


def chunk_text(
    text: str,
    chunk_words: int | None = None,
    overlap_words: int | None = None,
) -> list[str]:

    chunk_size = (
        chunk_words
        or settings.rag_chunk_words
    )

    overlap = (
        overlap_words
        or settings.rag_chunk_overlap_words
    )

    if overlap >= chunk_size:
        raise ValueError(
            "Chunk overlap must be "
            "smaller than chunk size."
        )

    words = text.split()

    if not words:
        return []

    chunks: list[str] = []

    start = 0

    while start < len(words):

        end = min(
            start + chunk_size,
            len(words),
        )

        chunk = " ".join(
            words[start:end]
        ).strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks