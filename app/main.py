from typing import Union

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from openai import (
    InternalServerError,
    RateLimitError,
    APIError,
)
from tenacity import (
    retry,
    stop_after_delay,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type,
)

from app.schemas.AssistantResponse import AssistantResponse
from app.schemas.Question import Question
from settings import Settings
from app.clients.llm import send_question

settings = Settings()
app = FastAPI()


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs", status_code=308)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@retry(
    stop=(stop_after_delay(10) | stop_after_attempt(3)),
    wait=wait_random_exponential(min=1, max=60),
    retry=(
        retry_if_exception_type(InternalServerError)
        | retry_if_exception_type(RateLimitError)
    ),
)
@app.post("/question")
async def read_question(request_body: Question) -> AssistantResponse:
    res: str
    try:
        res = await send_question(request_body)
    except RateLimitError as e:
        return AssistantResponse(text=e.response.text)
    except InternalServerError as e:
        return AssistantResponse(text=e.response.text)
    except APIError as e:
        return AssistantResponse(text=e.body.__str__())

    return AssistantResponse(text=res)
