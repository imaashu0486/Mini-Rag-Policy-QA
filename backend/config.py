from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    QDRANT_URL: str
    QDRANT_API_KEY: str
    QDRANT_COLLECTION: str = "policylens_chunks"

settings = Settings()
