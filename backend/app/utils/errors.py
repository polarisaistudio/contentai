# backend/app/utils/errors.py
class ContentAIException(Exception):
    def __init__(self, message: str, code: str, status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)

class RateLimitExceeded(ContentAIException):
    def __init__(self):
        super().__init__(
            message="Rate limit exceeded. Please try again later.",
            code="RATE_LIMIT_EXCEEDED",
            status_code=429
        )

class LLMError(ContentAIException):
    def __init__(self, detail: str):
        super().__init__(
            message=f"LLM generation failed: {detail}",
            code="LLM_ERROR",
            status_code=500
        )

class InvalidTemplateError(ContentAIException):
    def __init__(self, template_id: str):
        super().__init__(
            message=f"Template not found: {template_id}",
            code="INVALID_TEMPLATE",
            status_code=404
        )

