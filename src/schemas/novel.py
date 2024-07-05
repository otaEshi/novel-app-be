from pydantic import BaseModel, ConfigDict
from datetime import datetime
import typing

class NovelFullInfo(BaseModel):
    id: str
    title: str
    genres: list[str]
    author: str
    authorId: str
    tags: list[str]
    image: str
    status: str
    views: int
    description: str
    updatedDate: typing.Any
    createdDate: typing.Any
    warning: bool
    chapters: int
    rating: float
    rating_count: int

class NovelFullInfoResponse(BaseModel):
    id: str
    title: str
    genres: list[str]
    author: str
    authorId: str
    tags: list[str]
    image: str
    status: str
    views: int
    description: str
    updatedDate: str
    createdDate: str
    warning: bool
    chapters: int
    rating: float
    rating_count: int    

class RatingForNovel(BaseModel):
    rating: float
    rating_count: int

class CreateNovelPayload(BaseModel):
    title: str
    genres: list[str]
    tags: list[str]
    image: str
    description: str

class CreateNovelInDB(BaseModel):
    title: str
    genres: list[int]
    tags: list[int]
    image: str
    description: str
    author_id: int
    is_warning: bool
    status: str

class GetFollowPayload(BaseModel):
    userId: str
    state: str # following, follower

class FollowResponse(BaseModel):
    id: str
    name: str
    avatar: str

class NovelList(BaseModel):
    novels: list[NovelFullInfo]