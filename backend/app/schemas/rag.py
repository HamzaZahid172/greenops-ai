from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class DocumentResponse(BaseModel):
    id: int
    filename: str
    content_type: str
    chunk_count: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class RAGSearchRequest(BaseModel):
    query: str = Field(
        min_length=2,
        max_length=2000,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
    )


class RAGSearchHit(BaseModel):
    document_id: int
    filename: str
    chunk_index: int
    content: str
    similarity: float


class RAGSearchResponse(BaseModel):
    query: str
    results: list[RAGSearchHit]


class RAGAskRequest(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=2000,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
    )


class RAGAskResponse(BaseModel):
    answer: str
    sources: list[RAGSearchHit]
    provider: str