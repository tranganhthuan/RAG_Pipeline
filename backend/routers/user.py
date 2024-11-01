from fastapi import APIRouter, Response, status
from fastapi import Depends, HTTPException, status, Header, Body, Path
from sqlmodel import Session
from .utils import validate_jwt, get_password_hash, get_session
from model.user import User
from configs.config import engine_user
from functools import partial

router = APIRouter()

get_session_user = partial(get_session, engine_user)


# User Routes
@router.post("/api/users")
def create_user(
        user: User,
        session: Session = Depends(get_session_user),
):
    user.password = get_password_hash(user.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/api/user")
def get_user(
        session: Session = Depends(get_session_user),
        authorization: str = Header(None),
):
    id = validate_jwt(authorization)
    user = session.get(User, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"id": id}


@router.post("/api/users/{id}")
def update_user(
        session: Session = Depends(get_session_user),
        id: str = Path(...),
        user: User = Body(...),
        authorization: str = Header(None),
):
    validate_jwt(authorization)
    existing_user = session.get(User, id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    existing_user.email = user.email or existing_user.email
    existing_user.name = user.name or existing_user.name
    existing_user.role = user.role or existing_user.role
    if user.password:
        existing_user.password = get_password_hash(user.password)
    session.add(existing_user)
    session.commit()
    session.refresh(existing_user)
    return existing_user
