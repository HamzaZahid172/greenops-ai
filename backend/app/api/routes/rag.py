from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Response,
    UploadFile,
    status,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.db.session import get_db

from app.repositories.rag import (
    delete_document,
    list_documents,
    save_document,
)

from app.schemas.rag import (
    DocumentResponse,
    RAGAskRequest,
    RAGAskResponse,
    RAGSearchRequest,
    RAGSearchResponse,
)

from app.services.ai.base import (
    AIProviderError,
)

from app.services.ai.ollama_provider import (
    OllamaProvider,
)

from app.services.rag.chunker import (
    chunk_text,
)

from app.services.rag.document_loader import (
    load_document_text,
)

from app.services.rag.embeddings import (
    embedding_provider,
)

from app.services.rag.prompts import (
    build_rag_prompt,
)

from app.services.rag.retriever import (
    search_knowledge_base,
)


router = APIRouter(
    prefix="/rag",
    tags=["Knowledge Base / RAG"],
)


ai_provider = OllamaProvider()


@router.post(
    "/documents",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file has no filename.",
        )

    try:
        content = await file.read()

        text = load_document_text(
            filename=file.filename,
            content=content,
        )

        chunks = chunk_text(text)

        if not chunks:
            raise ValueError(
                "Document produced no chunks."
            )

        embeddings = (
            await embedding_provider.embed_texts(
                chunks
            )
        )

        document = await save_document(
            session=db,
            filename=file.filename,
            content_type=(
                file.content_type
                or "application/octet-stream"
            ),
            chunks=chunks,
            embeddings=embeddings,
        )

        return document

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except AIProviderError as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "Embedding provider is "
                "currently unavailable."
            ),
        ) from exc

    finally:
        await file.close()


@router.get(
    "/documents",
    response_model=list[DocumentResponse],
)
async def get_documents(
    db: AsyncSession = Depends(get_db),
):
    return await list_documents(db)


@router.delete(
    "/documents/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_document(
    document_id: int,
    db: AsyncSession = Depends(get_db),
):
    deleted = await delete_document(
        session=db,
        document_id=document_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.post(
    "/search",
    response_model=RAGSearchResponse,
)
async def search_documents(
    request: RAGSearchRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        results = await search_knowledge_base(
            session=db,
            query=request.query,
            top_k=request.top_k,
        )

        return RAGSearchResponse(
            query=request.query,
            results=results,
        )

    except AIProviderError as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "Embedding provider is "
                "currently unavailable."
            ),
        ) from exc


@router.post(
    "/ask",
    response_model=RAGAskResponse,
)
async def ask_documentation(
    request: RAGAskRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        sources = await search_knowledge_base(
            session=db,
            query=request.question,
            top_k=request.top_k,
        )

        if not sources:
            return RAGAskResponse(
                answer=(
                    "The available documentation "
                    "does not contain enough "
                    "information to answer this "
                    "question."
                ),
                sources=[],
                provider="ollama",
            )

        prompt = build_rag_prompt(
            question=request.question,
            sources=sources,
        )

        answer = await ai_provider.generate(
            prompt
        )

        return RAGAskResponse(
            answer=answer,
            sources=sources,
            provider="ollama",
        )

    except AIProviderError as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "AI or embedding provider is "
                "currently unavailable."
            ),
        ) from exc