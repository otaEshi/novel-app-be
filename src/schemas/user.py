from pydantic import BaseModel, ConfigDict
from datetime import datetime
from src.schemas.library import LibraryFullInfo
from src.schemas.review import ReviewFullInfo

class UserBase(BaseModel):
    username: str
    name: str

    # model_config = ConfigDict(from_attributes=True)

class CurrentUserResponse(BaseModel):
    id: str
    name: str
    username: str
    admin_type: int
    avatar: str

class UserInDB(UserBase):
    hashed_password: str


class UserInput(UserBase):
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    name: str

class UserCreateInDB(BaseModel):
    username: str
    name: str
    hashed_password: str
    admin_type: int
    created_date: datetime

class UserEditRight(BaseModel):
    user_id: str
    target_user_id: str
    admin_type: int

class UserFullInfo(BaseModel):
    id: str
    name: str
    username: str
    library: list[LibraryFullInfo]
    reviews: list[ReviewFullInfo]
    followers: list[str]
    following: list[str]
    avatar: str
    admin_type: int
    createDate: str

class FollowPayload(BaseModel):
    userId: str
    followId: str

class FollowReponse(BaseModel):
    id: str
    name: str
    avatar: str