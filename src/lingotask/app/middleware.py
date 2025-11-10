from app.exceptions import Error
from app.schemas import ErrorResponse
from fastapi import Request
from fastapi.responses import JSONResponse


async def error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Error as e:
        return JSONResponse(
            status_code=e.status_code,
            content=ErrorResponse(
                error_code=e.code,
                message=str(e),
            ).model_dump(),
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error_code='INTERNAL_ERROR',
                message=str(e),
            ).model_dump(),
        )
