from fastapi import HTTPException


class LLMBaseError(HTTPException):
    def __init__(self, status_code: int, message: str, retry_after: str):
        super().__init__(status_code, detail=message)
        self.retry_after = retry_after


class LLMRateLimitedError(LLMBaseError):
    pass


class LLMPermissionDeniedError(LLMBaseError):
    pass


class LLMInternalError(LLMBaseError):
    pass
