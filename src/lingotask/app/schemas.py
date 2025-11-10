from typing import List, Optional

from pydantic import BaseModel, Field


class VocabularyItem(BaseModel):
    english: str = Field(..., description='Term in English')
    chinese: str = Field(..., description='Chinese equivalent')
    explanation: str = Field(..., description='One-sentence Chinese explanation')


class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, description='English text to be translated')
    output_format: Optional[str] = Field(default='json', description='"json" or "word"')
    include_vocabulary: Optional[bool] = Field(default=True, description='Whether to extract vocabulary')


class TranslateResponse(BaseModel):
    success: bool
    translation: str
    vocabulary: List[VocabularyItem] = []
    word_document_url: Optional[str] = None


class ErrorResponse(BaseModel):
    success: bool = False
    error_code: str
    message: str
