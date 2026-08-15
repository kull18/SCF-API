from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:regiber123@localhost:5432/scf"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()