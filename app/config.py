import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "4000"))
    TIMEOUT_SECONDS: int = int(os.getenv("TIMEOUT_SECONDS", "25"))
    MAX_EXTRACT_CHARS: int = int(os.getenv("MAX_EXTRACT_CHARS", "20000"))
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))

settings = Settings()
