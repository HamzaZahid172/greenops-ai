from app.schemas.rag import (
    RAGSearchHit,
)


def build_rag_prompt(
    question: str,
    sources: list[RAGSearchHit],
) -> str:

    context = "\n\n".join(
        (
            f"SOURCE: {source.filename}\n"
            f"CHUNK: {source.chunk_index}\n"
            f"{source.content}"
        )
        for source in sources
    )

    return f"""
You are GreenOps AI.

Answer the user's question using ONLY
the supplied documentation.

QUESTION

{question}


DOCUMENTATION

{context}


RULES

1. Do not invent information.
2. Do not use facts that are not present
   in the supplied documentation.
3. If the documentation is insufficient,
   say so clearly.
4. Mention the relevant source filename
   when useful.
5. Never claim an infrastructure action
   has already been performed.
6. Keep the answer technical and concise.

ANSWER
""".strip()