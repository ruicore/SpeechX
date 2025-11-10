from app.config import settings
from app.middleware import error_handler
from app.schemas import TranslateRequest, TranslateResponse
from app.services.translation import translate
from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title='LingoTask — Module 1', version='1.0.0')

app.middleware('http')(error_handler)

api = APIRouter(prefix='/api/v1')


@api.post('/translate', response_model=TranslateResponse)
async def translate_endpoint(req: TranslateRequest):
    return await translate(req)


app.include_router(api)

app.mount(
    '/downloads',
    StaticFiles(directory=str(settings.download_dir)),
    name='downloads',
)

if __name__ == '__main__':
    ...
