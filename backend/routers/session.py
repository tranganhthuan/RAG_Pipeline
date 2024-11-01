from functools import partial

from configs.config import ADMIN_EMAIL, ADMIN_PASSWORD, engine_user
from fastapi import APIRouter, Body, Depends, Header, HTTPException, status
from model.user import User
from sqlmodel import Session, select

from .utils import create_access_token, get_session, verify_password

router = APIRouter()

get_session_user = partial(get_session, engine_user)


# Authentication Routes
@router.post("/api/session")
def login(
    email: str = Body(...),
    password: str = Body(...),
    session: Session = Depends(get_session_user),
):
    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        access_token = create_access_token(data={"sub": "admin"})
        return {"jwt_token": access_token, "is_admin": True}

    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": user.id})
    return {"jwt_token": access_token, "is_admin": False}


@router.delete("/api/session")
def logout(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token"
        )
    return {"message": "Logout successful"}
