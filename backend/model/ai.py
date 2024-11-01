from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from uuid import uuid4

class RAGQuery(BaseModel):
    text: str
    model: str


class RAGResponse(BaseModel):
    answer: str
    semantic_context: str
    semantic_metadata: str
    keyword_context: str
    keyword_metadata: str

class RAGResponseWithUser(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    query: str
    answer: str
    semantic_context: str
    semantic_metadata: str
    keyword_context: str
    keyword_metadata: str
    user_id: str

class ConvertPath(BaseModel):
    name: str


class ConvertResponse(BaseModel):
    job_id: str
