from openai import AsyncOpenAI, RateLimitError, APIError, PermissionDeniedError
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionUserMessageParam,
    ChatCompletionSystemMessageParam,
)
from tenacity import (
    retry,
    stop_after_delay,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type,
)

from app.schemas import Question
from app.schemas.llm.errors import (
    LLMRateLimitedError,
    LLMInternalError,
    LLMPermissionDeniedError,
)
from settings import Settings

settings = Settings()

llm_client = AsyncOpenAI(api_key=settings.LLM_API_KEY, base_url=settings.LLM_BASE_URL)


@retry(
    stop=(stop_after_delay(10) | stop_after_attempt(3)),
    wait=wait_random_exponential(min=1, max=60),
    retry=(
        retry_if_exception_type(LLMInternalError)
        | retry_if_exception_type(LLMRateLimitedError)
    ),
)
async def send_question(question: Question) -> str:
    system_msg: ChatCompletionSystemMessageParam = {
        "role": "system",
        "content": settings.SYSTEM_MESSAGE,
    }

    user_msg: ChatCompletionUserMessageParam = {
        "role": "user",
        "content": question.text,
    }

    try:
        response: ChatCompletion = await llm_client.chat.completions.create(
            model=settings.LLM_MODEL, messages=[system_msg, user_msg]
        )
        return response.choices[0].message.content
    except RateLimitError as e:
        print(e)
        retry_after: str = "0"
        if e.response:
            retry_after = e.response.headers.get("x-ratelimit-reset-tokens", "1")
        raise LLMRateLimitedError(message=str(e), retry_after=retry_after)
    except APIError as e:
        print(e)
        raise LLMInternalError(f"Internal OpenAI error: {str(e)}")
    except PermissionDeniedError as e:
        print(e)
        raise LLMPermissionDeniedError()
