import os
import uuid

from fastapi import APIRouter
from pydantic import BaseModel
from redis import Redis
from rq import Queue
from configs.config import REDIS_URL
from server.services.convert import convert_service

router = APIRouter()
convert_queue = Queue("convert", connection=Redis.from_url(REDIS_URL))


class ConvertPath(BaseModel):
    name: str


class Response(BaseModel):
    message: str


@router.post("/convert", response_model=Response)
async def convert_rag(query: ConvertPath):
    convert_job_id = f"convert-{uuid.uuid4()}"
    convert_queue.enqueue(
        "server.workers.convert.convert_file",
        args=(query.name, convert_job_id),
        job_id=convert_job_id,
    )
    return Response(message=convert_job_id)


@router.delete("/delete_document/{name}")
async def delete_document(name: str):
    convert_service.remove_document(name + ".md")
    return Response(message="Document deleted")


@router.get("/get_uploaded_documents")
async def get_documents():
    documents = os.listdir("data/pdfs")
    documents = [doc.replace(".pdf", "") for doc in documents if doc.endswith(".pdf")]
    processed_documents = convert_service.get_all_documents()
    processed_documents = [doc.replace(".md", "") for doc in processed_documents]
    documents = list(set(documents) - set(processed_documents))
    return {"documents": documents}


@router.get("/get_rag_documents")
async def get_rag_documents():
    documents = convert_service.get_all_documents()
    documents = [doc.replace(".md", "") for doc in documents]
    return {"documents": documents}
