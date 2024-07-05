from pydantic import BaseModel

from src.schemas.novel import NovelFullInfo

class LibraryFullInfo(BaseModel):
    id: str
    userId: str
    title: str
    isPublic: bool
    novels: list[NovelFullInfo]

class LibraryList(BaseModel):
    list: list[LibraryFullInfo]

class RemoveNovelFromListPayload(BaseModel):
    userId: str
    listId: str
    novelId: str

class CreateListPayload(BaseModel):
    userId: str
    title: str
    isPublic: bool

class AddNovelToListPayload(BaseModel):
    userId: str
    listId: str
    novelId: str

class DeleteLibraryListPayload(BaseModel):
    userId: str
    listId: str

class UpdateLibraryListPrivacyPayload(BaseModel):
    userId: str
    listId: str
    isPublic: bool

class UpdateLibraryListTitlePayload(BaseModel):
    userId: str
    listId: str
    title: str