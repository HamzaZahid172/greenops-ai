from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.repositories.rag import (
    semantic_search,
)

from app.schemas.rag import (
    RAGSearchHit,
)

from app.services.rag.embeddings import (
    embedding_provider,
)


async def search_knowledge_base(
    session: AsyncSession,
    query: str,
    top_k: int,
) -> list[RAGSearchHit]:

    embeddings = (
        await embedding_provider
        .embed_texts([query])
    )

    query_embedding = embeddings[0]

    rows = await semantic_search(
        session,
        query_embedding,
        top_k,
    )

    results: list[
        RAGSearchHit
    ] = []

    for (
        chunk,
        document,
        distance,
    ) in rows:

        similarity = round(
            1.0 - float(distance),
            4,
        )

        results.append(
            RAGSearchHit(
                document_id=document.id,
                filename=document.filename,
                chunk_index=(
                    chunk.chunk_index
                ),
                content=chunk.content,
                similarity=similarity,
            )
        )

    return results