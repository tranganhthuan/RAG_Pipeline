import httpx
from configs.config import AI_SERVER_URL, engine_rag
from fastapi import APIRouter, Header, HTTPException
from model.ai import RAGQuery, RAGResponse, RAGResponseWithUser

from .utils import get_session, validate_jwt

router = APIRouter()

session_rag = get_session(engine_rag)


@router.post("/api/query", response_model=RAGResponse)
async def query_rag(query: RAGQuery, authorization: str = Header(None)):
    try:
        # Validate JWT token
        user_id = validate_jwt(authorization)

        # Call the RAG service
        response = await httpx.AsyncClient().post(
            AI_SERVER_URL + "/query", json={"text": query.text, "model": query.model}
        )
        answer = response.json()
        answer_with_user = answer.copy()
        answer_with_user["user_id"] = user_id
        answer_with_user["query"] = query.text
        answer_with_user = RAGResponseWithUser(**answer_with_user)

        session_rag.add(answer_with_user)
        session_rag.commit()

        return RAGResponse(**answer)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/history", response_model=list[RAGResponseWithUser])
async def get_rag_history():
    try:
        history = session_rag.query(RAGResponseWithUser).all()
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
