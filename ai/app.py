import uvicorn
from fastapi import FastAPI
from loguru import logger
from configs.config import AI_SERVER_URL
from server.routers import router_list
from urllib.parse import urlparse

app = FastAPI(
    title="ESG RAG API",
    docs_url=None,  # Disable docs in production
    redoc_url=None,  # Disable redoc
)


@app.on_event("startup")
async def startup_event():
    for router in router_list:
        logger.info(f"Including router: {router}")
        app.include_router(router)


if __name__ == "__main__":
    port = urlparse(AI_SERVER_URL).port
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)
