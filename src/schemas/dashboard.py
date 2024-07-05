from pydantic import BaseModel

class ViewPerNovelPayload(BaseModel):
    authorId: str

class ViewPerGenreResponse(BaseModel):
    genre: str
    viewCount: int

class ViewPerNovelPayload(BaseModel):
    authorId: str

class CommentPerChapterPayload(BaseModel):
    novelId: str

class UserPerTimePayload(BaseModel):
    year: str
    isNewAccount: bool

class UserPerTime(BaseModel):
    userCount: list[int] # list of user count per month - 12 months 

class UserPerTimeResponse(BaseModel):
    month: str
    userPerTime: UserPerTime