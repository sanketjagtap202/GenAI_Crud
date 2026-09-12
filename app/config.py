from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "user_crud_db"
    upload_dir: str = "uploads"
    max_file_size_mb: int = 5

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
