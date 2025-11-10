import pytest
from app.schemas import TranslateRequest
from app.services.translation import translate


@pytest.mark.asyncio
async def test_translate_success_word(monkeypatch, tmp_path):
    """Test main translation flow with word output and vocabulary."""

    async def fake_call_llm(prompt: str, input_text: str):
        return {
            'translation': f"翻译:{input_text[:10]}",
            'vocabulary': [
                {'english': 'Machine Learning', 'chinese': '机器学习', 'explanation': '一种从数据中学习的方法'}
            ],
        }

    monkeypatch.setattr('app.services.translation.call_llm', fake_call_llm)

    # reduce download dir to tmp
    from app.config import settings

    settings.download_dir = tmp_path

    req = TranslateRequest(text='Machine learning is great.', output_format='word', include_vocabulary=True)
    resp = await translate(req)
    assert resp.success is True
    assert resp.translation.startswith('翻译:')
    assert len(resp.vocabulary) == 1
    assert resp.word_document_url is not None


@pytest.mark.asyncio
async def test_translate_no_vocab(monkeypatch):
    async def fake_call_llm(prompt: str, input_text: str):
        return {'translation': '翻译', 'vocabulary': []}

    monkeypatch.setattr('app.services.translation.call_llm', fake_call_llm)

    req = TranslateRequest(text='Short text.', output_format='json', include_vocabulary=False)
    resp = await translate(req)
    assert resp.success is True
    assert resp.vocabulary == []
