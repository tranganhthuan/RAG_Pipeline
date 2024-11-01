import os
import dotenv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
dotenv.load_dotenv()

BACKEND_SERVER_URL = os.getenv("BACKEND_SERVER_URL", "http://127.0.0.1:8002")
AI_SERVER_URL = os.getenv("AI_SERVER_URL", "http://127.0.0.1:8007")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6380")
VECTOR_STORE_URL = os.getenv("VECTOR_STORE_URL", "http://localhost:8000")

UPLOAD_FOLDER = os.getenv(
    "UPLOAD_FOLDER", os.path.join(PROJECT_ROOT, "backend/uploads")
)
VECTOR_STORE_FOLDER = os.getenv(
    "VECTOR_STORE_FOLDER", os.path.join(PROJECT_ROOT, "ai/data/vector_store")
)
PDF_FOLDER = os.getenv("PDF_FOLDER", os.path.join(PROJECT_ROOT, "ai/data/pdfs"))
MARKDOWN_FOLDER = os.getenv(
    "MARKDOWN_FOLDER", os.path.join(PROJECT_ROOT, "ai/data/markdowns/text")
)
IMAGE_FOLDER = os.getenv(
    "IMAGE_FOLDER", os.path.join(PROJECT_ROOT, "ai/data/markdowns/images")
)

CONVERTER = os.getenv("CONVERTER", "llama_parse")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")