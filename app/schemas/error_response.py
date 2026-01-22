from pydantic import BaseModel


class ErrorResponse(BaseModel):
    status_code: int = 500
    detail: str = "No error info provided"
    retry_after: str | None
