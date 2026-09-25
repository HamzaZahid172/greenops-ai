from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GreenOps AI"
    app_version: str = "0.1.0"
    app_environment: str = "development"

    api_v1_prefix: str = "/api/v1"

    database_url: str = (
        "postgresql+asyncpg://localhost/greenops_ai"
    )

    carbon_api_base_url: str = (
        "https://api.carbonintensity.org.uk"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()