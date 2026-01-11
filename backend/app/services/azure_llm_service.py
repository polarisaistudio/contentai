# backend/app/services/azure_llm_service.py
from openai import AzureOpenAI, AsyncAzureOpenAI
import os

class AzureLLMService:
    def __init__(self):
        self.client = AsyncAzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-15-preview"
        )
        self.deployment = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o-mini")

    async def generate(self, request: ContentRequest) -> ContentResponse:
        response = await self.client.chat.completions.create(
            model=self.deployment,  # Use deployment name, not model name
            messages=[
                {"role": "system", "content": self._build_system_prompt(request.content_type, request.tone)},
                {"role": "user", "content": request.prompt}
            ],
            max_tokens=request.max_tokens,
        )
        return ContentResponse(
            content=response.choices[0].message.content,
            model=self.deployment,
            usage={"total_tokens": response.usage.total_tokens}
        )
