# backend/app/services/llm_factory.py
from enum import Enum
from typing import Protocol, AsyncGenerator

class LLMProvider(str, Enum):
    OPENAI = "openai"
    AZURE = "azure"
    ANTHROPIC = "anthropic"

class LLMServiceProtocol(Protocol):
    async def generate(self, request: ContentRequest) -> ContentResponse: ...
    async def generate_stream(self, request: ContentRequest) -> AsyncGenerator[str, None]: ...

def get_llm_service(provider: LLMProvider = LLMProvider.OPENAI) -> LLMServiceProtocol:
    """Factory function to get appropriate LLM service."""
    if provider == LLMProvider.OPENAI:
        from .llm_service import llm_service
        return llm_service
    elif provider == LLMProvider.AZURE:
        from .azure_llm_service import AzureLLMService
        return AzureLLMService()
    elif provider == LLMProvider.ANTHROPIC:
        from .anthropic_service import AnthropicService
        return AnthropicService()
    else:
        raise ValueError(f"Unknown provider: {provider}")
