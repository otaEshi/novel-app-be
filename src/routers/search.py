from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.novel import NovelList
from src.schemas.search import SearchNovelPayload
from src.database.dependencies import DBSession
from src import crud
# from src.routers.user import get_novel

router = APIRouter()

@router.get("/search")
def search_novels(db: DBSession, payload: SearchNovelPayload):
    novels = crud.search_novel(db, payload)

    novel_list = []
    for novel in novels:
        novel_full_info = get_novel(novel.id, db)
        if novel_full_info:
            novel_list.append(novel_full_info)

    return_novel_list = NovelList(novels=[])
    return return_novel_list