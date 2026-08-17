from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:regiber123@localhost:5432/scf"
    SECRET_KEY: str = "change-me-in-.env"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ONESIGNAL_APP_ID: str = ""
    ONESIGNAL_REST_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()