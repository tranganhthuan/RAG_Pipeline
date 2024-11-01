from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from server.services.rag import rag_service

router = APIRouter()


class Query(BaseModel):
    text: str
    model: str


class Response(BaseModel):
    answer: str
    semantic_context: str
    semantic_metadata: str
    keyword_context: str
    keyword_metadata: str

@router.post("/query", response_model=Response)
async def query_rag(query: Query):
    try:
        answer = rag_service.invoke(query.text, query.model)
        return Response(
            answer=answer.answer,
            semantic_context=answer.semantic_context,
            semantic_metadata=answer.semantic_metadata,
            keyword_context=answer.keyword_context,
            keyword_metadata=answer.keyword_metadata,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
