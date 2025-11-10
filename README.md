# LingoTask — Module 1 (Intelligent Translation API)

FastAPI implementation of the **required** module:

- English → Chinese translation
- Professional vocabulary extraction
- Optional Word (docx) export
- Full OpenAPI docs at `/docs`
- Tests (`pytest`) and curl scripts provided

This project is **Module 1 only** (no audio/video code).

---

## Deliverables
1. Translation Prompt: variable `PROMPTS` in file `src/lingotask/prompts.py` 
2. Core Code: files under `src/`
3. Test Code: files under `src/tests/`, test case use `pytest` and were used to test basic functionality instead of LLM.
4. Test Data & Word samples: [sample.txt](src/lingotask/sample.txt) and file [translation_20251110_212357.docx](src/lingotask/downloads/translation_20251110_212357.docx)
5. Screenshots: ![Operation Screenshots.png](src/lingotask/Operation%20Screenshots.png)
6. AI Conversation Records: https://chatgpt.com/share/69120869-7d28-8000-bbe4-58044c60ddc0

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Fill DEEPSEEK_API_KEY or VOLCENGINE_API_KEY

uvicorn app.main:app --reload
# Open http://127.0.0.1:8000/docs
```

## Environment

Edit `.env` to configure one LLM provider:

```ini
DEEPSEEK_API_KEY=
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat

VOLCENGINE_API_KEY=
VOLCENGINE_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
VOLCENGINE_MODEL=ep-translate-1 # (example; replace with real name)

# General
APP_DOWNLOAD_DIR=./downloads
MAX_TEXT_CHARS=10000
REQUEST_TIMEOUT_SECONDS=60
RETRY_MAX_ATTEMPTS=2
RETRY_BACKOFF_SECONDS=1.0
```

## Endpoints

### POST `/api/v1/translate`

Request:
```json
{
  "text": "Machine learning is a subset of artificial intelligence ...",
  "output_format": "word",
  "include_vocabulary": true
}
```

Response:
```json
{
  "success": true,
  "translation": "机器学习是人工智能的一个子集...",
  "vocabulary": [
    {"english":"Machine Learning","chinese":"机器学习","explanation":"..."}
  ],
  "word_document_url": "/downloads/translation_YYYYMMDD_HHMMSS.docx"
}
```

### Errors
Uniform error structure:
```json
{
  "success": false,
  "error_code": "LLM_BAD_JSON",
  "message": "The LLM did not return valid JSON."
}
```

## Deliverables mapping

- **Translation Prompt**: `prompts/translation_en.txt`
- **Core Code**: `app/*`
- **Test Code**: `tests/*`, `scripts/curl_translate.sh`
- **Test Data & Word samples**: `samples/input.txt` and files under `downloads/` after calling with `output_format:"word"`
- **Screenshots**: Swagger `/docs` and curl responses
- **AI Conversation Records**: paste your DeepSeek/VolcEngine share link in your submission email

---
