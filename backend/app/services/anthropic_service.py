# backend/app/services/anthropic_service.py
import anthropic
import os

class AnthropicService:
    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20241022"

    async def generate(self, request: ContentRequest) -> ContentResponse:
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=request.max_tokens,
            system=self._build_system_prompt(request.content_type, request.tone),
            messages=[
                {"role": "user", "content": request.prompt}
            ]
        )

        return ContentResponse(
            content=response.content[0].text,
            model=self.model,
            usage={
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            }
        )

    async def generate_stream(self, request: ContentRequest):
        async with self.client.messages.stream(
            model=self.model,
            max_tokens=request.max_tokens,
            system=self._build_system_prompt(request.content_type, request.tone),
            messages=[{"role": "user", "content": request.prompt}]
        ) as stream:
            async for text in stream.text_stream:
                yield text

