from fastapi import APIRouter, HTTPException, Depends 
from pydantic import BaseModel
from typing import Annotated
from src.schemas.user import UserBase, UserInput
from src import crud
from src.database.dependencies import DBSession
from datetime import timedelta, datetime
from src import crud
from fastapi.security import OAuth2PasswordBearer
from src.security import validate_token
from src.schemas.user import CurrentUserResponse, UserFullInfo
from src.schemas.novel import GetFollowPayload, NovelFullInfo, CreateNovelPayload, NovelFullInfoResponse
from src.schemas.review import ReviewFullInfo
from src.schemas.report import ReportWarningFullInfoResponse, ReportNovelFullInfoResponse, ReportReviewFullInfoResponse, ReportCommentFullInfoResponse, ReportChapterFullInfoResponse
from src.schemas.comment import CommentFullInfo
from src.schemas.chapter import DeleteChapter, UpdateChapterPayload, CreateChapterPayload, ChangeNovelStatusPayload

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db_session: DBSession):
    """
        Get the current user

        Args:
            token (str): The token of the user.
    """

    token_data = validate_token(token)
    if token_data.user_name is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials, user_id is None", headers={"WWW-Authenticate": "Bearer"})
    user = crud.get_user_via_username(db_session, username=token_data.user_name)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return_user = CurrentUserResponse(
        id=str(user.id),
        name=user.name,
        username=user.username,
        admin_type=user.admin_type,
        avatar=user.avatar
    )
    return return_user

def get_novel(novel_id: str, db_session: DBSession) -> NovelFullInfo:
    novel = crud.get_novel(db_session, novel_id)
    author = crud.get_user_via_id(db_session, novel.author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    
    chapter_count = crud.get_chapter_count(db_session, novel_id)
    rating = crud.get_novel_rating(db_session, novel_id)
    
    return_novel = NovelFullInfo(
        id=str(novel.id),
        title=novel.title or "Untitled",
        genres=novel.genres or [],
        tags=novel.tags or [],
        image=novel.image or "",
        description=novel.description or "",
        updatedDate=str(novel.last_chapter_created_date) if novel.last_chapter_created_date else "N/A",
        createdDate=str(novel.created_date) if novel.created_date else "N/A",
        authorId=str(novel.author_id) or "",
        status=novel.status,
        warning=novel.is_warning if novel.is_warning is not None else False,
        views=novel.view_count or 0,
        author=author.name or "Unknown author",
        chapters=chapter_count or 0,
        rating=rating.rating or 0.0,
        rating_count=rating.rating_count or 0
    )
    return return_novel

def get_comment_for_report(comment_id: str, db_session: DBSession):
    comment = crud.get_comment_via_id(db_session, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    user = crud.get_user_via_id(db_session, str(comment.user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    chapter = crud.get_chapter_via_id(db_session, str(comment.chapter_id))
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return_comment = CommentFullInfo(
        commentId= str(comment.id),
        userId= str(comment.user_id),
        name = user.name,
        novelId= str(chapter.novel_id),
        chapterId= str(comment.chapter_id),
        content= comment.content,
        createDate= str(comment.created_date),
        liked= comment.liked,
    )
    return return_comment

@router.get("/me")
def read_users_me(
    current_user: CurrentUserResponse = Depends(get_current_user)
):
    return current_user

@router.get("/{user_id}")
def get_user(user_id: str, db_session: DBSession):
    user = crud.get_user_via_id(db_session, user_id)
    if user is None or user.admin_type != 0:
        raise HTTPException(status_code=404, detail="User not found")
    library = crud.get_library_via_user_id(db_session, user_id)
    reviews = crud.get_review_via_user_id(db_session, user_id)

    followers_str = [str(follower_id) for follower_id in user.followers]
    following_str = [str(following_id) for following_id in user.following]

    response_user = UserFullInfo(
        id=str(user.id),
        name=user.name,
        username=user.username,
        library=library or [],
        reviews=reviews or [],
        followers=followers_str or [],
        following=following_str or [],
        avatar=user.avatar or "",
        admin_type=user.admin_type or 0,
        createDate=str(user.created_date),
    )
    return response_user    

@router.patch("/novel")
def update_novel_info(
    userId: str,
    novelId: str,
    title: str,
    genres: list[str],
    tags: list[str],
    image: str,
    description: str,
    db_session: DBSession
):
    novel = crud.update_novel_info(db_session, userId, novelId, title, genres, tags, image, description)
    # author = crud.get_user_via_id(db_session, userId)
    # if author is None:
    #     raise HTTPException(status_code=404, detail="Author not found")
    # chapter_count = crud.get_chapter_count(db_session, novelId)
    # rating = crud.get_novel_rating(db_session, novelId)
    # return_novel = NovelFullInfo(
    #     id=str(novel.id),
    #     title=novel.title,
    #     genres=novel.genres,
    #     tags=novel.tags,
    #     image=novel.image,
    #     description=novel.description,
    #     updatedDate=str(novel.last_chapter_created_date),
    #     createDate=str(novel.created_date),
    #     authorId=str(novel.author_id),
    #     status=novel.status,
    #     warning=novel.is_warning,
    #     views=novel.view_count,
    #     author=author.name,
    #     chapters=chapter_count,
    #     rating= rating.rating,
    #     rating_count= rating.rating_count
    # )
    return_novel = get_novel(novelId, db_session)
    return return_novel

@router.get("/original-works/{user_id}")
def get_original_works(user_id: str, db_session: DBSession):
    novels = crud.get_original_works(db_session, user_id)
    if novels is None:
        raise HTTPException(status_code=404, detail="No novels found")
    author = crud.get_user_via_id(db_session, user_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return_novels = []
    for novel in novels:
        # chapter_count = crud.get_chapter_count(db_session, novel.id)
        # rating = crud.get_novel_rating(db_session, novel.id)
        # novel_full_info = NovelFullInfo(
        #     id= str(novel.id),
        #     title= novel.title,
        #     genres= novel.genres,
        #     image= novel.image,
        #     description= novel.description,
        #     updatedDate= str(novel.last_chapter_created_date),
        #     createDate= str(novel.created_date),
        #     authorId= str(novel.author_id),
        #     status= novel.status,
        #     warning= novel.is_warning,
        #     views= novel.view_count,
        #     author= author.name,
        #     chapters= chapter_count,
        #     rating= rating.rating,
        #     rating_count= rating.rating_count
        # )
        novel_full_info = get_novel(novel.id, db_session)
        return_novels.append(novel_full_info)
    
    return return_novels

@router.get("/reviews/{user_id}")
def get_user_review(user_id: str, db_session: DBSession):
    reviews = crud.get_review_via_user_id(db_session, user_id)
    if reviews is None:
        raise HTTPException(status_code=404, detail="No reviews found")
    user = crud.get_user_via_id(db_session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return_reviews = [ReviewFullInfo]
    for review in reviews:
        novel = crud.get_novel_via_id(db_session, review.novel_id)
        if novel is None:
            raise HTTPException(status_code=404, detail="Novel not found")
        
        review_full_info = ReviewFullInfo(
            id= str(review.id),
            userId= str(review.user_id),
            novelId= str(review.novel_id),
            review= review.review,
            rating= review.rating,
            liked= review.liked,
            createAt= str(review.created_date),
            novelTitle= novel.title,
            userAvatar= user.avatar,
            userName= user.name,
            updateDate= str(review.updated_date),
        )
        return_reviews.append(review_full_info)
    return return_reviews

@router.patch("/")
def update_user_profile(user_id: str, user_name: str, user_avatar: str, db_session: DBSession):
    user = crud.update_user_profile(db_session, user_id, user_name, user_avatar)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    library = crud.get_library_via_user_id(db_session, user_id)
    reviews = crud.get_review_via_user_id(db_session, user_id)
    response_user = UserFullInfo(
        id=str(user.id),
        name=user.name,
        username=user.username,
        library=library or [],
        reviews=reviews or [],
        followers=user.followers or [],
        following=user.following or [],
        avatar=user.avatar,
        admin_type=user.admin_type,
        createDate=str(user.created_date),
    )
    return response_user

@router.get("/report/report")
def get_report(target_id: str, user_id: str, type: str, db_session: DBSession):
    reports = crud.get_report_via_user_and_target_id(db_session, target_id)
    if not reports:
        raise HTTPException(status_code=404, detail="No reports found")
    
    target_mapping = {
        # "novel": "novelId",
        # "review": "reviewId",
        # "comment": "commentId",
        "chapter": "chapterId",
        "warning": "adminId",
    }
    
    if type not in target_mapping:
        raise HTTPException(status_code=400, detail="Invalid report type")

    return_reports = []

    for report in reports:
        if report.type != type:
            continue
        
        if type == "warning":
            return_report = ReportWarningFullInfoResponse(
                reportId=str(report.id),
                userId=str(report.user_id),
                novelId=str(report.target_id),
                reason=report.reason,
                processed=report.processed
            )
    
        elif type == "chapter":
            chapter = crud.get_chapter_via_id(db_session, str(report.target_id))
            if not chapter:
                raise HTTPException(status_code=404, detail="Chapter not found")
            return_report = ReportChapterFullInfoResponse(
                reportId=str(report.id),
                userId=str(report.user_id),
                chapterId=str(report.target_id),
                chapterTitle=chapter.title,
                reason=report.reason,
                processed=report.processed
            )

        return_reports.append(return_report)

    if not return_reports:
        raise HTTPException(status_code=404, detail=f"No {type.capitalize()} reports found for target ID {target_id}")

    return return_reports

@router.post("/create-novel")
def create_novel(payload: CreateNovelPayload, db_session: DBSession, current_user = Depends(get_current_user)):
    
    novel= crud.create_novel(db_session, payload, current_user.id)

    novel_full_info = NovelFullInfo(
        id= str(novel.id),
        title= novel.title,
        genres= novel.genres,
        tags= novel.tags,
        image= novel.image,
        description= novel.description,
        updatedDate= novel.last_chapter_created_date,
        createdDate= novel.created_date,
        authorId= str(novel.author_id),
        status= novel.status,
        warning= novel.is_warning,
        views= 0,
        author= current_user.name,
        chapters= 0,
        rating= 0,
        rating_count= 0
    )
    return novel_full_info

@router.post("/create-chapter")
def create_chapter(payload: CreateChapterPayload, db_session: DBSession, current_user = Depends(get_current_user)):
    crud.create_chapter(db_session, payload, current_user.id)
    return_novel = get_novel(payload.novelId, db_session)
    return return_novel

@router.patch("/chapter-status")
def change_chapter_status(db_session: DBSession, payload: ChangeNovelStatusPayload):
    crud.change_chapter_status(db_session, payload)

    res = crud.get_chapter(db_session, payload.chapterId)
    return res

@router.patch("/chapter-update")
def update_chapter(db_session: DBSession, payload: UpdateChapterPayload):
    crud.update_chapter(db_session, payload)
    res = crud.get_chapter(db_session, payload.chapterId)
    return res

@router.delete("/chapter")
def delete_chapter(db_session: DBSession, payload: DeleteChapter):
    novel = crud.delete_chapter(db_session, payload)
    res = get_novel(novel.id, db_session)
    return res

@router.post("/follow")
def get_follow(db_session: DBSession, payload: GetFollowPayload):
    res = crud.get_follow(db_session, payload)

    return res