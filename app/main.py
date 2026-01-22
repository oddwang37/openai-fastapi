from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from app.clients.llm import send_question
from app.schemas import Question, AssistantResponse, ErrorResponse
from app.schemas.llm.errors import (
    LLMRateLimitedError,
    LLMInternalError,
    LLMPermissionDeniedError,
)
from settings import Settings

settings = Settings()
app = FastAPI()


@app.exception_handler(LLMRateLimitedError)
async def llm_rate_limited_error_handler(request: Request, exc: LLMRateLimitedError):
    return ErrorResponse(
        status_code=exc.status_code, detail=exc.detail, retry_after=exc.retry_after
    )


@app.exception_handler(LLMInternalError)
async def llm_client_error_handler(request: Request, exc: LLMInternalError):
    return ErrorResponse(
        status_code=exc.status_code, detail=exc.detail, retry_after=exc.retry_after
    )


@app.exception_handler(LLMPermissionDeniedError)
async def llm_permission_denied_error_handler(
    request: Request, exc: LLMPermissionDeniedError
):
    return ErrorResponse(
        status_code=exc.status_code, detail=exc.detail, retry_after=exc.retry_after
    )


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs", status_code=308)


@app.post("/question")
async def read_question(request_body: Question) -> AssistantResponse:
    res = await send_question(request_body)
    return AssistantResponse(text=res)
