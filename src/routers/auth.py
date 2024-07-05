from fastapi import APIRouter, HTTPException, Depends, status, Header
from sqlalchemy import select
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Optional
from typing import Annotated
from src.crud import create_user
from src.database.dependencies import DBSession
from src.database.models.users import User
from src.schemas.user import UserBase, UserInput, UserCreate
from src.security import validate_token, create_access_token, create_refresh_token
from src.schemas.schemas import User as UserSchema, Novel as NovelSchema, Review as ReviewSchema, Report as ReportSchema
from src.schemas.token import Token
from src import crud
from datetime import timedelta
from src.configurations import settings
from jose import JWTError, jwt

router = APIRouter()

@router.post("/signup", response_model=str)
def create_user_api(
    user_in: UserCreate,
    db_session: DBSession,
) -> str:
    try:
        user_created = create_user(db_session, user_in)
        if user_created:
            return "User creation successful"
    except Exception as e:
        raise e
    
@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db_session: DBSession
) -> Token:
    user = crud.authenticate_user(db_session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.username})
    return Token(access_token=access_token, refresh_token=refresh_token,token_type="bearer")

@router.post("/refresh_token", response_model=Token, tags=["Users"])
async def refresh_token(
    refresh_token: Annotated[str, Header(...)],
    db_session: DBSession
):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials, user_id is None", headers={"WWW-Authenticate": "Bearer"})
        user = crud.get_user_via_username(db_session, username=username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        access_token_expires = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        new_refresh_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer", "refresh_token": new_refresh_token}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials, JWTError", headers={"WWW-Authenticate": "Bearer"})
