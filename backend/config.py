import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "policylens_chunks")

    CHUNK_TARGET_TOKENS = 900
    CHUNK_OVERLAP_TOKENS = 120

settings = Settings()
