from src.database.dependencies import DBSession
from fastapi import APIRouter, Depends, HTTPException, status
from src import crud
from src.schemas.novel import NovelList
from src.routers.user import get_novel

router = APIRouter()

@router.get("/tag-list")
def get_tag_list(db: DBSession):
    tags = crud.get_tag_list(db)
    return tags

@router.get("/{tag_name}")
def get_novels_by_tag(tag_name: str, db: DBSession):
    novels = crud.get_novels_by_tag(db, tag_name)

    enriched_novels = []
    for novel in novels:
        novel= get_novel(novel.id, db)  # Assuming get_novel returns details for a single novel
        enriched_novels.append(novel)

    return_novel = NovelList(novels=enriched_novels)
    return return_novel