from passlib.context import CryptContext
from sqlmodel import create_engine
import os
import dotenv

dotenv.load_dotenv()

# Secret key and JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

# Dependency and DB Setup
sqlite_file_name_user = os.getenv("SQLITE_FILE_NAME_USER", "user_database.db")
sqlite_url_user = f"sqlite:///{sqlite_file_name_user}"
engine_user = create_engine(sqlite_url_user, connect_args={"check_same_thread": False})

sqlite_file_name_rag = os.getenv("SQLITE_FILE_NAME_RAG", "rag_database.db")
sqlite_url_rag = f"sqlite:///{sqlite_file_name_rag}"
engine_rag = create_engine(sqlite_url_rag, connect_args={"check_same_thread": False})

# Utility Functions
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

FRONTEND_SERVER_URL = os.getenv("FRONTEND_SERVER_URL", "http://127.0.0.1:5173")
BACKEND_SERVER_URL = os.getenv("BACKEND_SERVER_URL", "http://127.0.0.1:8002")
AI_SERVER_URL = os.getenv("AI_SERVER_URL", "http://127.0.0.1:8007")

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@admin.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
