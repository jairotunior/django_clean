from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "Test API"
    app_version: str = "0.1.1"
    api_v1_prefix: str = "/api/v1"
    # Optional for tests that don't hit the database
    database_url: str | None = None

    time_zone: str = "America/Bogota"


settings = Settings()