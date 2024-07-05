from fastapi import APIRouter, HTTPException, Depends 
from pydantic import BaseModel
from typing import Annotated
from src.schemas.user import UserBase, UserInput
from src import crud
from src.database.dependencies import DBSession
from datetime import timedelta, datetime
from src import crud
from fastapi.security import OAuth2PasswordBearer
from src.security import validate_token
from src.schemas.user import CurrentUserResponse, UserFullInfo
from src.schemas.novel import NovelFullInfo

router = APIRouter()

