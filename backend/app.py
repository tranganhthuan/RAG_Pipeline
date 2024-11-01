from functools import partial
from urllib.parse import urlparse

import uvicorn
from configs.config import FRONTEND_SERVER_URL, BACKEND_SERVER_URL, engine_rag, engine_user
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import RAGResponseWithUser, User
from routers import router_list
from routers.utils import create_db_and_tables

create_db_and_tables_user = partial(create_db_and_tables, User, engine_user)
create_db_and_tables_rag = partial(
    create_db_and_tables, RAGResponseWithUser, engine_rag
)

app = FastAPI(
    title="ESG RAG API",
    on_startup=[create_db_and_tables_user, create_db_and_tables_rag],
)

origins = [
    FRONTEND_SERVER_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in router_list:
    app.include_router(router)

if __name__ == "__main__":
    port = urlparse(BACKEND_SERVER_URL).port
    uvicorn.run(app, host="0.0.0.0", port=port)
