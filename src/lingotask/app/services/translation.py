from app.config import settings
from app.exceptions import BadRequestError
from app.llm import call_llm
from app.schemas import TranslateRequest, TranslateResponse, VocabularyItem
from app.services.word_export import build_docx
from app.utils import split_text_for_llm
from prompts import PROMPTS


def _merge_translation(parts: list[str]) -> str:
    return '\n'.join(p.strip() for p in parts if p and p.strip())


def _dedup_vocab(vocab: list[VocabularyItem]) -> list[VocabularyItem]:
    seen = set()
    out = []
    for v in vocab:
        key = (v.english.lower().strip(), v.chinese.strip())
        if key in seen:
            continue
        seen.add(key)
        out.append(v)
    return out


async def translate(req: TranslateRequest) -> TranslateResponse:
    text = req.text.strip()
    if not text:
        raise BadRequestError('Text is empty.')
    if len(text) > settings.max_text_chars:
        chunks = split_text_for_llm(text)
    else:
        chunks = [text]

    translations: list[str] = []
    vocab_accum: list[VocabularyItem] = []

    for ch in chunks:
        llm_out = await call_llm(prompt=PROMPTS, input_text=ch)
        t = llm_out.get('translation', '').strip()
        translations.append(t)
        if req.include_vocabulary:
            raw = llm_out.get('vocabulary', []) or []
            for it in raw:
                try:
                    vocab_accum.append(VocabularyItem(**it))
                except Exception:  # noqa
                    continue

    final_translation = _merge_translation(translations)
    final_vocab = _dedup_vocab(vocab_accum) if req.include_vocabulary else []

    word_url = None
    if req.output_format == 'word':
        out_path = build_docx(
            text=text,
            translation=final_translation,
            vocabulary=final_vocab,
            download_dir=settings.download_dir,
        )
        word_url = f"/downloads/{out_path.name}"

    return TranslateResponse(
        success=True,
        translation=final_translation,
        vocabulary=final_vocab,
        word_document_url=word_url,
    )
