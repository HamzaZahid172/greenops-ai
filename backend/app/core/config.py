from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    app_name: str = "GreenOps AI"
    app_version: str = "0.1.0"
    app_environment: str = "development"

    api_v1_prefix: str = "/api/v1"

    database_url: str = (
        "postgresql+asyncpg://localhost/greenops_ai"
    )

    cors_origins: str = (
        "http://localhost:5173,"
        "http://127.0.0.1:5173"
    )

    carbon_api_base_url: str = (
        "https://api.carbonintensity.org.uk"
    )

    ai_provider: str = "ollama"

    ollama_base_url: str = (
        "http://localhost:11434"
    )

    ollama_model: str = "llama3.2:3b"

    ollama_embedding_model: str = (
        "nomic-embed-text"
    )

    rag_embedding_dimension: int = 768
    rag_chunk_words: int = 350
    rag_chunk_overlap_words: int = 60
    rag_default_top_k: int = 5
    rag_max_file_size_mb: int = 5

    @property
    def cors_origin_list(
        self,
    ) -> list[str]:
        return [
            origin.strip()
            for origin
            in self.cors_origins.split(",")
            if origin.strip()
        ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()