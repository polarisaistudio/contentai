# backend/app/services/llm_service.py
import os
from openai import OpenAI, AsyncOpenAI
from typing import AsyncGenerator
from pydantic import BaseModel

class ContentRequest(BaseModel):
    prompt: str
    content_type: str  # "blog", "social", "email", "marketing"
    tone: str = "professional"  # "professional", "casual", "formal"
    max_tokens: int = 1000

class ContentResponse(BaseModel):
    content: str
    model: str
    usage: dict

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.async_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"  # Cost-effective default

    def _build_system_prompt(self, content_type: str, tone: str) -> str:
        prompts = {
            "blog": f"You are an expert blog writer. Write in a {tone} tone. Create engaging, well-structured content with clear headings.",
            "social": f"You are a social media expert. Write in a {tone} tone. Create punchy, engaging content optimized for engagement.",
            "email": f"You are an email copywriter. Write in a {tone} tone. Create clear, action-oriented emails.",
            "marketing": f"You are a marketing copywriter. Write in a {tone} tone. Create persuasive, benefit-focused content.",
        }
        return prompts.get(content_type, prompts["blog"])

    async def generate(self, request: ContentRequest) -> ContentResponse:
        """Generate content (non-streaming)."""
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._build_system_prompt(request.content_type, request.tone)},
                {"role": "user", "content": request.prompt}
            ],
            max_tokens=request.max_tokens,
            temperature=0.7,
        )

        return ContentResponse(
            content=response.choices[0].message.content,
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
        )

    async def generate_stream(self, request: ContentRequest) -> AsyncGenerator[str, None]:
        """Generate content with streaming."""
        stream = await self.async_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._build_system_prompt(request.content_type, request.tone)},
                {"role": "user", "content": request.prompt}
            ],
            max_tokens=request.max_tokens,
            temperature=0.7,
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

# Singleton instance
llm_service = LLMService()
