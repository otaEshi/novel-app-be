from fastapi import APIRouter
from src.database.dependencies import DBSession
from src import crud
from src.schemas.dashboard import UserPerTimeResponse, UserPerTimePayload, CommentPerChapterPayload, ViewPerNovelPayload

router = APIRouter()

@router.get("/view-genre")
def view_genre(db: DBSession):
    genre_views = crud.get_view_per_genre(db)
    return genre_views

@router.get("/view-tag")
def view_tag(db: DBSession):
    tag_views = crud.get_view_per_tag(db)
    return tag_views

@router.get("/view-novel")
def view_novel(db: DBSession, payload: ViewPerNovelPayload):
    novel_views = crud.get_view_per_novel(db, payload)
    return novel_views

@router.get("/review-novel")
def review_novle(db: DBSession):
    novel_reviews = crud.get_review_per_novel(db)
    return novel_reviews

@router.get("comment-chapter")
def comment_chapter(db: DBSession, payload: CommentPerChapterPayload):
    chapter_comments = crud.get_comment_per_chapter(db, payload)
    return chapter_comments

@router.get("user-time")
def user_time(db: DBSession, payload: UserPerTimePayload):
    user_per_time = crud.get_user_per_time(db, payload)
    return UserPerTimeResponse(month=payload.year, userPerTime=user_per_time)