from .user import router as user_router
from .session import router as session_router
from .ai import router as ai_router
from .upload import router as upload_router

router_list = [user_router, session_router, ai_router, upload_router]
