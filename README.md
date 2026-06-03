# SpeechX / LingoTask

SpeechX currently contains the `lingotask` module: a FastAPI-based intelligent translation service for English-to-Chinese technical content.

The project demonstrates a small but complete AI application surface: prompt design, request/response schemas, LLM integration, vocabulary extraction, optional Word export, API documentation, sample data, screenshots, and tests that protect the non-LLM behavior.

## Features

- English to Chinese translation for technical text.
- Professional vocabulary extraction.
- Optional `.docx` export for translated output.
- FastAPI application with interactive docs at `/docs`.
- Prompt definition in `src/lingotask/prompts.py`.
- Sample input and generated Word output under `src/lingotask/`.
- Pytest coverage for core request handling and deterministic behavior.

## Project Layout

```text
src/
├── lingotask/
│   ├── app/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── llm.py
│   │   ├── main.py
│   │   ├── middleware.py
│   │   ├── schemas.py
│   │   └── utils.py
│   ├── prompts.py
│   ├── requirements.txt
│   └── sample.txt
└── tests/
    └── test_translate.py
```

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r src/lingotask/requirements.txt

uvicorn src.lingotask.app.main:app --reload
```

Then open:

- API docs: `http://127.0.0.1:8000/docs`
- Sample data: `src/lingotask/sample.txt`

## Test

```bash
pytest src/tests
```

The tests focus on the deterministic service behavior around the API layer and helper code rather than calling the LLM provider directly.

## Screenshots

![JSON response screenshot](src/lingotask/screenshots_json.png)

![Word export screenshot](src/lingotask/screenshots_word.png)

## Notes

- This repository currently covers the translation module only.
- Audio/video speech-to-speech work is intentionally outside the current module.
- AI conversation record: https://chatgpt.com/share/6912095c-f3fc-8000-a7cd-c53889437b82
