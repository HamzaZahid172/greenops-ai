from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.db.models import (
    DocumentChunk,
    DocumentRecord,
)


async def save_document(
    session: AsyncSession,
    filename: str,
    content_type: str,
    chunks: list[str],
    embeddings: list[list[float]],
) -> DocumentRecord:

    document = DocumentRecord(
        filename=filename,
        content_type=content_type,
        chunk_count=len(chunks),
    )

    session.add(document)

    await session.flush()

    for index, (
        chunk,
        embedding,
    ) in enumerate(
        zip(
            chunks,
            embeddings,
            strict=True,
        )
    ):

        session.add(
            DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                content=chunk,
                embedding=embedding,
            )
        )

    await session.commit()

    await session.refresh(document)

    return document


async def list_documents(
    session: AsyncSession,
) -> list[DocumentRecord]:

    result = await session.execute(
        select(DocumentRecord)
        .order_by(
            DocumentRecord.created_at.desc()
        )
    )

    return list(
        result.scalars().all()
    )


async def delete_document(
    session: AsyncSession,
    document_id: int,
) -> bool:

    result = await session.execute(
        delete(DocumentRecord)
        .where(
            DocumentRecord.id
            == document_id
        )
        .returning(DocumentRecord.id)
    )

    deleted_id = result.scalar_one_or_none()

    await session.commit()

    return deleted_id is not None


async def semantic_search(
    session: AsyncSession,
    query_embedding: list[float],
    top_k: int,
):

    distance = (
        DocumentChunk.embedding
        .cosine_distance(
            query_embedding
        )
        .label("distance")
    )

    statement = (
        select(
            DocumentChunk,
            DocumentRecord,
            distance,
        )
        .join(
            DocumentRecord,
            DocumentRecord.id
            == DocumentChunk.document_id,
        )
        .order_by(distance)
        .limit(top_k)
    )

    result = await session.execute(
        statement
    )

    return result.all()