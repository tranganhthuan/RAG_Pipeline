from sqlmodel import SQLModel, Field
from uuid import uuid4


class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    email: str = Field(index=True)
    password: str
    name: str
    role: str