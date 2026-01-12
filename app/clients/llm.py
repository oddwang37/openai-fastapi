from openai import AsyncOpenAI
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionUserMessageParam,
    ChatCompletionSystemMessageParam,
)

from app.schemas.Question import Question
from settings import Settings

settings = Settings()

api_key = settings.OPENAI_KEY or settings.OLLAMA_KEY
openai_client = AsyncOpenAI(api_key=settings.OPENAI_KEY)


async def send_question(question: Question) -> str:
    system_msg: ChatCompletionSystemMessageParam = {
        "role": "system",
        "content": settings.SYSTEM_MESSAGE,
    }

    user_msg: ChatCompletionUserMessageParam = {
        "role": "user",
        "content": question.text,
    }

    response: ChatCompletion = await openai_client.chat.completions.create(
        model="gpt-4o", messages=[system_msg, user_msg]
    )

    return response.choices[0].message.content
