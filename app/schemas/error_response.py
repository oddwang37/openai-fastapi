from typing import Optional

from starlette.responses import JSONResponse


class ErrorResponse(JSONResponse):
    def __init__(
        self,
        status_code: int,
        retry_after: Optional[str],
        detail: str = "No error info provided",
    ):
        super().__init__(status_code=status_code, content={"detail": detail})
        self.detail: str = detail
        self.retry_after: str | None = retry_after
