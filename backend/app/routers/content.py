# backend/app/routers/content.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from ..services.llm_factory import get_llm_service, LLMProvider
from ..services.llm_service import ContentRequest, ContentResponse

router = APIRouter(prefix="/api/content", tags=["Content"])

@router.post("/generate", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    """Generate content (non-streaming)."""
    try:
        service = get_llm_service(LLMProvider.OPENAI)
        return await service.generate(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate/stream")
async def generate_content_stream(request: ContentRequest):
    """Generate content with streaming response."""
    service = get_llm_service(LLMProvider.OPENAI)

    async def stream_generator():
        async for chunk in service.generate_stream(request):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
