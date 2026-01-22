class LLMBaseError(Exception):
    def __init__(self, detail: str, retry_after: str = 10):
        super().__init__(detail)
        self.retry_after = retry_after


class LLMRateLimitedError(LLMBaseError):
    pass


class LLMPermissionDeniedError(LLMBaseError):
    pass


class LLMInternalError(LLMBaseError):
    pass
