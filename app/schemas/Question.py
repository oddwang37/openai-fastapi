from pydantic import BaseModel, Field


class Question(BaseModel):
    text: str = Field(min_length=5, max_length=500, description="Question text")
