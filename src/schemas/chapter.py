from pydantic import BaseModel
from datetime import datetime

class ChapterFullInfo(BaseModel):
    id: str
    title: str
    content: str  # path to chapter file
    createdDate: datetime
    chapter: int # chapter number, when create new chapter, chapter number = totla chapter + 1, start from 1
    status: str # published, deleted

class CreateChapterPayload(BaseModel):
    novelId: str
    title: str
    content: str # chapter content
    status: str # published, deleted

class ChangeNovelStatusPayload(BaseModel):
    userId: str
    chapterId: str
    status: str

class ChapterResponseFull(BaseModel):
    id: str
    title: str
    content: str
    status: str
    chapter: int
    createdAt: datetime

class UpdateChapterPayload(BaseModel):
    id: str
    userId: str
    title: str
    content: str
    status: str

class DeleteChapter(BaseModel):
    userId: str
    chapterId: str