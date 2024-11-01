import os

import httpx
from configs.config import AI_SERVER_URL, UPLOAD_DIR
from fastapi import APIRouter, File, Header, HTTPException, UploadFile
from model.ai import ConvertResponse
from routers.utils import validate_jwt

os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()


@router.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...), authorization: str = Header(None)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        user_id = validate_jwt(authorization)
        if user_id != "admin":
            raise HTTPException(status_code=403, detail="Forbidden")
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        response = httpx.post(AI_SERVER_URL + "/convert", json={"name": file.filename})
        return {"message": "Successfully uploaded"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/response_convert")
async def response_convert(convert_response: ConvertResponse):
    return {"message": convert_response.job_id}


@router.get("/api/get_uploaded_documents")
async def get_documents(authorization: str = Header(None)):
    try:
        user_id = validate_jwt(authorization)
        if user_id != "admin":
            raise HTTPException(status_code=403, detail="Forbidden")
        response = httpx.get(AI_SERVER_URL + "/get_uploaded_documents")
        return response.json()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/get_rag_documents")
async def get_rag_documents(authorization: str = Header(None)):
    try:
        user_id = validate_jwt(authorization)
        if user_id != "admin":
            raise HTTPException(status_code=403, detail="Forbidden")
        response = httpx.get(AI_SERVER_URL + "/get_rag_documents")
        return response.json()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/api/delete_document/{name}")
async def delete_document(name: str, authorization: str = Header(None)):
    try:
        user_id = validate_jwt(authorization)
        if user_id != "admin":
            raise HTTPException(status_code=403, detail="Forbidden")
        httpx.delete(AI_SERVER_URL + f"/delete_document/{name}")
        return {"message": "Document deleted"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
