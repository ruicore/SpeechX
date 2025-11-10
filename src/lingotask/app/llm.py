import asyncio
import json

import httpx
from app.config import settings
from app.exceptions import ConfigError, LLMError


def _extract_json(text: str) -> dict:
    start = text.find('{')
    end = text.rfind('}')
    if start == -1 or end == -1:
        raise LLMError('LLM did not return JSON.', code='LLM_BAD_JSON')
    snippet = text[start : end + 1]
    try:
        data = json.loads(snippet)
    except Exception as e:
        raise LLMError(f"JSON parse error: {e}", code='LLM_BAD_JSON')

    data.setdefault('translation', '')
    data.setdefault('vocabulary', [])
    return data


async def _post_json(url: str, headers: dict, payload: dict):
    async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
        return await client.post(url, headers=headers, json=payload)


async def call_llm(prompt: str, input_text: str) -> dict:
    last_err = None
    headers = {'Authorization': f"Bearer {settings.deepseek_api_key}"}
    url = f"{settings.deepseek_base_url}/v1/chat/completions"
    payload = {
        'messages': [
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': input_text},
        ],
        'model': settings.deepseek_model,
        'temperature': 0.2,
    }

    for attempt in range(settings.retry_max_attempts + 1):
        try:
            r = await _post_json(url, headers, payload)
            if r.status_code // 100 != 2:
                raise LLMError(f"DeepSeek error {r.status_code}: {r.text}", code='LLM_UPSTREAM_ERROR')

            content = r.json()['choices'][0]['message']['content']
            try:
                return _extract_json(content)
            except LLMError:
                payload['messages'][-1]['content'] = input_text + '\n\nRespond JSON only. No commentary.'
                r = await _post_json(url, headers, payload)
                content = r.json()['choices'][0]['message']['content']
                return _extract_json(content)

        except (LLMError, ConfigError) as e:
            last_err = e
            if attempt < settings.retry_max_attempts:
                await asyncio.sleep(settings.retry_backoff_seconds)
                continue
            raise

        except Exception as e:
            last_err = LLMError(str(e), code='LLM_UPSTREAM_ERROR')
            if attempt < settings.retry_max_attempts:
                await asyncio.sleep(settings.retry_backoff_seconds)
                continue
            raise last_err

    raise last_err or LLMError('Unknown LLM failure')
