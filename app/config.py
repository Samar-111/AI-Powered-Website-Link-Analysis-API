import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    @property
    def GEMINI_API_KEY(self) -> str:
        key = os.getenv("GEMINI_API_KEY", "")
        return key.strip().strip('"').strip("'")

    @property
    def GEMINI_MODEL(self) -> str:
        return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    @property
    def HOST(self) -> str:
        return os.getenv("HOST", "0.0.0.0")

    @property
    def PORT(self) -> int:
        return int(os.getenv("PORT", "4000"))

    @property
    def TIMEOUT_SECONDS(self) -> int:
        return int(os.getenv("TIMEOUT_SECONDS", "25"))

    @property
    def MAX_EXTRACT_CHARS(self) -> int:
        return int(os.getenv("MAX_EXTRACT_CHARS", "20000"))

    @property
    def CACHE_TTL_SECONDS(self) -> int:
        return int(os.getenv("CACHE_TTL_SECONDS", "3600"))

settings = Settings()
