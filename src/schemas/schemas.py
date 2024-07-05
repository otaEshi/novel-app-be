from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    avatar: Optional[str]
    admin_type: int

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_date: datetime

    class Config:
        from_attributes = True

class NovelBase(BaseModel):
    author_id: int
    title: str
    image: Optional[str]
    genres: List[str]
    tags: List[str]
    description: Optional[str]

class NovelCreate(NovelBase):
    pass

class Novel(NovelBase):
    id: int
    created_date: datetime

    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    user_id: int
    novel_id: int
    content: str
    rating: int
    liked: Optional[List[int]]

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    created_date: datetime

    class Config:
        from_attributes = True

class ReportBase(BaseModel):
    user_id: int
    target_id: int
    report_type: str
    reason: str
    processed: bool

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    id: int
    created_date: datetime

    class Config:
        from_attributes = True
