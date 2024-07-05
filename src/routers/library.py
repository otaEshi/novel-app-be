from fastapi import APIRouter
from src.database.dependencies import DBSession
from src import crud
from src.schemas.library import UpdateLibraryListTitlePayload, UpdateLibraryListPrivacyPayload, DeleteLibraryListPayload, AddNovelToListPayload, CreateListPayload, LibraryList, LibraryFullInfo, RemoveNovelFromListPayload
from src.routers.user import get_novel

router = APIRouter()

@router.get("/list/{user_id}")
def get_library_list(db: DBSession, user_id: int):
    libraries = crud.get_library_list(db, user_id)
    library_list = []
    for library in libraries:
        novel_list = []
        for id in library.novels:
            novel = get_novel(id, db)
            if novel:
                novel_list.append(novel)
        library_list = LibraryFullInfo (
            id= str(library.id),
            title= library.title,
            userId= str(library.user_id),
            isPublic= library.is_public,
            novels= novel_list,
        )
        library_list.append(library_list)
    return library_list

@router.patch("/list/novel/remove")
def remove_novel_from_list(db: DBSession, payload: RemoveNovelFromListPayload):
    crud.remove_novel_from_list(db, payload)
    return {"message": "Novel removed from list"}

@router.post("/list")
def create_list(db: DBSession, payload: CreateListPayload):
    novel_list = crud.create_novel_list(db, payload)

    return novel_list

@router.patch("/list/novel/add")
def add_novel_to_list(db: DBSession, payload: AddNovelToListPayload):
    novel_list = crud.add_novel_to_list(db, payload)
    novels = []
    for id in novel_list.novels:
        novel = get_novel(id, db)
        if novel:
            novels.append(novel)

    return_list = LibraryFullInfo(
        id= str(novel_list.id),
        title= novel_list.title,
        userId= str(novel_list.user_id),
        isPublic= novel_list.is_public,
        novels= novels,
    )

    return return_list

@router.delete("/list")
def delete_library_list(db: DBSession, payload: DeleteLibraryListPayload):
    crud.delete_library_list(db, payload)
    
    return {"message": "List deleted"}

@router.patch("list/privacy")
def update_list_privacy(db: DBSession, payload: UpdateLibraryListPrivacyPayload):
    novel_list = crud.update_library_list_privacy(db, payload)

    novels = []
    for id in novel_list.novels:
        novel = get_novel(id, db)
        if novel:
            novels.append(novel)

    return_list = LibraryFullInfo(
        id= str(novel_list.id),
        title= novel_list.title,
        userId= str(novel_list.user_id),
        isPublic= novel_list.is_public,
        novels= novels,
    )

    return return_list

@router.patch("/list/title")
def update_list_title(db: DBSession, payload: UpdateLibraryListTitlePayload):
    novel_list = crud.update_library_list_title(db, payload)

    novels = []
    for id in novel_list.novels:
        novel = get_novel(id, db)
        if novel:
            novels.append(novel)

    return_list = LibraryFullInfo(
        id= str(novel_list.id),
        title= novel_list.title,
        userId= str(novel_list.user_id),
        isPublic= novel_list.is_public,
        novels= novels,
    )

    return return_list