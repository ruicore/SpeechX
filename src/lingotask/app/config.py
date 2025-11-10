import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    deepseek_api_key: str | None = os.getenv('DEEPSEEK_API_KEY')
    deepseek_base_url: str = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
    deepseek_model: str = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')

    download_dir: Path = Path(os.getenv('APP_DOWNLOAD_DIR', './downloads')).resolve()
    max_text_chars: int = int(os.getenv('MAX_TEXT_CHARS', '10000'))
    request_timeout_seconds: int = int(os.getenv('REQUEST_TIMEOUT_SECONDS', '60'))
    retry_max_attempts: int = int(os.getenv('RETRY_MAX_ATTEMPTS', '2'))
    retry_backoff_seconds: float = float(os.getenv('RETRY_BACKOFF_SECONDS', '1.0'))


settings = Settings()
settings.download_dir.mkdir(parents=True, exist_ok=True)
