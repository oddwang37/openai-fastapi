from pydantic import BaseModel, Field


class AssistantResponse(BaseModel):
    text: str = Field(description="Response from AI assistant")
