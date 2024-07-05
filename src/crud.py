import os
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
import datetime
from src.database import User, Library, Novel, Review, Report, Chapter, Comment, Genre, Tag
from src.schemas.blogs import BlogInDB
from src.schemas.novel import GetFollowPayload, FollowResponse
from src.schemas.chapter import DeleteChapter, UpdateChapterPayload, ChangeNovelStatusPayload, CreateChapterPayload
from src.schemas.user import UserCreate, FollowPayload
from src.schemas.comment import DeleteCommentPayload
from src.schemas.library import UpdateLibraryListTitlePayload, UpdateLibraryListPrivacyPayload, DeleteLibraryListPayload, AddNovelToListPayload, RemoveNovelFromListPayload, CreateListPayload
from src.schemas.admin import AdjustAccountRightPayload, AdminHandleReportPayload
from src.schemas.dashboard import UserPerTime, UserPerTimePayload, CommentPerChapterPayload, ViewPerNovelPayload
from src.security import get_hashed_password, verify_password
import logging
from src.schemas.novel import RatingForNovel, CreateNovelPayload, CreateNovelInDB
from src.schemas.report import SendWarningPayload
from src.schemas.search import SearchNovelPayload
from sqlalchemy import func, extract

def get_user_via_username(db: Session, username: str):
    """
    Retrieve a user from the database based on the user_id.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to retrieve.

    Returns:
        User: The user object if found, None otherwise.
    """
    return db.query(User).filter(User.username == username).first()

def get_user_via_id(db: Session, user_id: str):
    """
    Retrieve a user from the database based on the user_id.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to retrieve.

    Returns:
        User: The user object if found, None otherwise.
    """
    return db.query(User).filter(User.id == int(user_id)).first()


def get_users(db: Session, 
                    admin_type: int,
                    user_name: str, ):
    """
    Retrieve a list of users from the database.

    Args:
        db (Session): The database session.
        skip (int, optional): Number of users to skip. Defaults to 0.
        limit (int, optional): Maximum number of users to retrieve. Defaults to 100.

    Returns:
        List[User]: A list of User objects.
    """

    search_params = {}
    if admin_type is not None and admin_type != 0:
        search_params["admin_type"] = admin_type
    if user_name is None:
        user_name = "" 
    print(user_name)
    query = db.query(User).filter_by(**search_params).filter(User.username.contains(user_name))
    
    result = query.all()
    return result

def create_user(db: Session, user: UserCreate):
#     """
#     Create a new user in the database.

#     Parameters:
#     - db (Session): The database session.
#     - user (UserCreate): The user data to be created.

#     Returns:
#     - User: The created user object.
#     """
#     hashed_password = get_hashed_password(user.password)

#     # Check for duplicate username
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="ERR_USERNAME_ALREADY_EXISTS")
    hashed_password = get_hashed_password(user.password)
    db_user = User(
        username=user.username,
        name=user.name,
        hashed_password=hashed_password,
        admin_type=0,
        avatar="temp",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# def update_user(db: Session, user: UserEdit, user_id: str):
#     """
#     Edit a user in the database.

#     Args:
#         db (Session): The database session.
#         user (UserEdit): The updated user data.
#         user_id (int): The ID of the user to edit.

#     Returns:
#         models.User: The edited user object.
#     """
#     db_user = db.query(User).filter(User.id == user_id).first()
#     attributes = ['name', 'date_of_birth', 'avatar_url']
#     for attr in attributes:
#         if getattr(user, attr):
#             setattr(db_user, attr, getattr(user, attr))
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def update_user_permissions(db: Session, user_id: str, user: UserEditRight):
#     """
#     Edit a user's permission in the database.

#     Args:
#         db (Session): The database session.
#         user_id (int): The ID of the user to edit.
#         user (UserEditPermission): The updated user permission data.

#     Returns:
#         models.User: The edited user object.
#     """
#     db_user = db.query(User).filter(User.id == int(user_id)).first()
#     if db_user is None:
#         return {"detail": "USER_NOT_FOUND"}
#     if user.is_content_admin is not None:
#         db_user.is_content_admin = user.is_content_admin
#         db.commit()
#         db.refresh(db_user)
#     return db_user

def update_user_profile (db: Session, user_id: str, user_name: str, user_avatar: str):
    """
    Edit a user's profile in the database.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user to edit.
        user_name (str): The updated user name.
        user_avatar (str): The updated user avatar.
    Returns:
        models.User: The edited user object.
    """
    check_user = db.query(User).filter(User.name == user_name).first()
    if check_user and check_user.id != int(user_id):
        raise HTTPException(status_code=400, detail="USERNAME_ALREADY_EXISTS")
    db_user = db.query(User).filter(User.id == int(user_id)).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")
    if user_name is not None:
        db_user.name = user_name
    if user_avatar is not None:
        db_user.avatar = user_avatar
    db.commit()
    db.refresh(db_user)
    return db_user
    
# def verify_password(plain_password, hashed_password):
#     """
#     Verify if the plain password matches the hashed password.

#     Args:
#         plain_password (str): The plain password to be verified.
#         hashed_password (str): The hashed password to compare against.

#     Returns:
#         bool: True if the plain password matches the hashed password, False otherwise.
#     """
#     return verify_password(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, password: str):

    user = db.query(User).filter(User.username == username).first()
    if not user:
        print("user not found")
        return False
    if not verify_password(password, user.hashed_password):
        print("password not verified")
        return False
    return user

def get_library_via_user_id(db: Session, user_id: str):

    return db.query(Library).filter(User.id == int(user_id)).first()

def get_review_via_user_id(db: Session, user_id: str):

    return db.query(Review).filter(User.id == int(user_id)).all()

def get_novel_via_id(db: Session, novel_id: str):

    return db.query(Novel).filter(User.id == int(novel_id)).first()

def update_novel_info(db: Session, user_id: str, novel_id: str, title: str, genres: list[str], tags: list[str], image: str, description: str):
    novel = db.query(Novel).filter(Novel.id == int(novel_id)).first()
    if novel is None:
        raise HTTPException(status_code=404, detail="Novel not found")
    if novel.author_id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    novel.title = title
    novel.genres = genres
    novel.tags = tags
    novel.image = image
    novel.description = description
    db.commit()
    db.refresh(novel)
    return novel

def get_chapter_count(db: Session, novel_id: str):

    return db.query(Chapter).filter(Chapter.novel_id == int(novel_id) and Chapter.status=="published").count()

def get_novel_rating(db: Session, novel_id: str):
    reviews =  db.query(Review).filter(Review.novel_id == int(novel_id)).all()
    if reviews:
        total_rating = sum(review.rating for review in reviews)
        rating_count = len(reviews)
        average_rating = total_rating / rating_count
    else:
        average_rating = 0.0
        rating_count = 0
    result = RatingForNovel(
        rating= average_rating,
        rating_count= rating_count
    )
    return result

def get_report_via_user_and_target_id(db: Session, target_id: str):
    return db.query(Report).filter(Report.target_id == int(target_id)).all()

def get_report_for_admin(db: Session):
    return db.query(Report).filter(Report.report_type.in_(["novel", "comment", "review"])).all()

def get_comment_via_id(db: Session, comment_id: str):
    return db.query(Comment).filter(Comment.id == int(comment_id)).first()

def get_chapter_via_id(db: Session, chapter_id: str):
    return db.query(Chapter).filter(Chapter.id == int(chapter_id)).first()

def create_novel(db: Session, payload: CreateNovelPayload, user_id: int):
    image = payload.image
    if image is None:
        image = "temp"
    db_novel = Novel(
        title=payload.title,
        genres=payload.genres,
        tags=payload.tags,
        image=image,
        description=payload.description,
        author_id=int(user_id),
        is_warning=False,
        status="ongoing",
        last_chapter_created_date=datetime.datetime.now(datetime.UTC),
        created_date=datetime.datetime.now(datetime.UTC)
    )
    db.add(db_novel)
    db.commit()
    db.refresh(db_novel)
    return db_novel

def create_chapter(db: Session, payload: CreateChapterPayload, user_id: str):
    novel = db.query(Novel).filter(Novel.id == int(payload.novelId)).first()
    if novel is None:
        raise HTTPException(status_code=404, detail="Novel not found")
    if novel.author_id != int(user_id):
        raise HTTPException(status_code=404, detail="User is not authorized to create chapters for this novel")
    novel.last_chapter_created_date = datetime.datetime.now(datetime.utc)
    db_chapter = Chapter(
        novel_id=int(payload.novelId),
        title=payload.title,
        status=payload.status,
        created_date=datetime.datetime.now(datetime.utc),
        chapter=db.query(Chapter).filter(Chapter.novel_id == int(payload.novelId)).count() + 1
    )
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    
    # 
    chapter_id = db_chapter.id
    content_path = f"./chapter_contents/{chapter_id}.txt"
    os.makedirs(os.path.dirname(content_path), exist_ok=True)
    
    with open(content_path, "w", encoding="utf-8") as f:
        f.write(payload.content)
    
    db_chapter.content = content_path
    db.commit()
    db.refresh(db_chapter)
    
    return db_chapter

def get_novel(db: Session, novel_id: str):
    novel = db.query(Novel).filter(Novel.id == int(novel_id)).first()
    if novel is None:
        raise HTTPException(status_code=404, detail="Novel not found")
    return novel

def change_chapter_status(db: Session, payload: ChangeNovelStatusPayload):
    chapter = db.query(Chapter).filter(Chapter.id == int(payload.chapterId)).first()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    chapter.status = payload.status
    db.commit()
    db.refresh(chapter)
    return chapter

def get_chapter(db: Session, chapter_id: str):
    # Retrieve the Chapter object from the database
    chapter = db.query(Chapter).filter(Chapter.id == int(chapter_id)).first()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    # Read the content from the file
    content_path = chapter.content
    if not os.path.exists(content_path):
        raise HTTPException(status_code=404, detail="Path to chapter not found")
    
    with open(content_path, "r", encoding="utf-8") as f:
        chapter_content = f.read()
    
    # Create a dictionary to return the chapter details including content
    chapter_details = {
        "id": chapter.id,
        "title": chapter.title,
        "status": chapter.status,
        "chapter": chapter.chapter,
        "created_date": chapter.created_date,
        "content": chapter_content
    }
    
    return chapter_details

def update_chapter(db: Session, payload: UpdateChapterPayload):
    # Retrieve the existing Chapter object from the database
    chapter = db.query(Chapter).filter(Chapter.id == int(payload.id)).first()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    # Update the Chapter object with the new values from the payload
    chapter.title = payload.title
    chapter.status = payload.status
    # Optionally, update the updated_date field
    # chapter.updated_date = datetime.utcnow()
    
    # Commit the changes to the database
    db.commit()
    db.refresh(chapter)
    
    # Write the new content to the file
    content_path = chapter.content
    if not os.path.exists(content_path):
        return None  # or raise HTTPException with 404 status
    
    with open(content_path, "w", encoding="utf-8") as f:
        f.write(payload.content)
    
    return chapter

def delete_chapter(db: Session, payload: DeleteChapter):
    # Query the Chapter object from the database
    chapter = db.query(Chapter).filter(Chapter.id == int(payload.id)).first()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    # Query the corresponding Novel object to check authorization
    novel = db.query(Novel).filter(Novel.id == chapter.novel_id).first()
    if novel is None:
        raise HTTPException(status_code=404, detail="Novel not found")
    
    # Check if the user is the author of the novel
    if novel.author_id != int(payload.userId):
        raise HTTPException(status_code=403, detail="Unauthorized access")
    
    # Delete the file associated with the chapter content
    content_path = chapter.content
    if os.path.exists(content_path):
        os.remove(content_path)

    # Delete the chapter from the database
    db.delete(chapter)
    db.commit()
    
    return novel

def get_follow(db: Session, payload: GetFollowPayload):
    try:
        user_id = int(payload.userId)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    # Query the user based on payload.userId
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    following = user.following if user.following is not None else []
    followers = user.followers if user.followers is not None else []
    # Determine which array to use based on payload.state
    if payload.state == "following":
        if not following:
            return []
        users_query = db.query(User).filter(User.id.in_(user.following))
    elif payload.state == "follower":
        if not followers:
            return []
        users_query = db.query(User).filter(User.id.in_(user.followers))
    else:
        raise HTTPException(status_code=400, detail="State must be 'following' or 'follower'")
    
    # Execute the query to get the users
    users = users_query.all()
    
    # Convert users to FollowResponse objects
    follow_responses = []
    for user in users:
        follow_response = FollowResponse(
            id=str(user.id),
            name=user.name,
            avatar=user.avatar or "",
        )
        follow_responses.append(follow_response)
    
    return follow_responses

def get_tag_list(db: Session):
    tags = db.query(Tag).all()
    
    tag_names = [tag.name for tag in tags]
    
    return tag_names

def get_novels_by_tag(db: Session, tag_name: str):
    tag = db.query(Tag).filter(Tag.name == tag_name).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    novels = db.query(Novel).filter(Novel.tags.contains(tag.id)).all()
    
    return novels

def get_genre_list(db: Session):
    genres = db.query(Genre).all()
    
    genre_names = [genre.name for genre in genres]
    
    return genre_names

def get_admin_list(db: Session):
    admins = db.query(User).filter(User.admin_type != 0).all()
    
    return admins

def adjust_admin_right(db: Session, payload: AdjustAccountRightPayload):
    user = db.query(User).filter(User.id == int(payload.currentuserId)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.admin_type != 2:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    target_user = db.query(User).filter(User.id == int(payload.userId)).first()
    target_user.admin_type = payload.admin_type
    db.commit()
    db.refresh(target_user)
    
    return target_user

def send_warning(db: Session, payload: SendWarningPayload):
    user = db.query(User).filter(User.id == int(payload.adminId)).first()
    if user.admin_type != 2 and user.admin_type != 1:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    novel = db.query(Novel).filter(Novel.id == int(payload.novelId)).first()
    novel.is_warning = True
    db.commit()
    db.refresh(novel)

    report = Report(
        user_id=int(payload.userId),
        target_id=int(novel.id),
        report_type="warning",
        reason=payload.reason,
        processed=False
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    
    return report

def handle_report(db: Session, payload: AdminHandleReportPayload):
    report = db.query(Report).filter(Report.id == int(payload.reportId)).first()

    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.user_id != int(payload.userId):
        raise HTTPException(status_code=403, detail="Unauthorized access")
    
    report.processed = payload.processed

    return report

def delete_comment(db: Session, payload: DeleteCommentPayload):
    comment = db.query(Comment).filter(Comment.id == int(payload.commentId)).first()
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    user = db.query(User).filter(User.id == int(payload.userId)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id != comment.user_id and user.admin_type == 0:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    
    db.delete(comment)
    db.commit()
    
    return comment

def search_novel(db: Session, payload: SearchNovelPayload):
    query = db.query(Novel)

    # Filtering based on payload criteria
    if payload.title:
        query = query.filter(func.lower(Novel.title).like(f"%{payload.title.lower()}%"))
    
    if payload.author:
        query = query.filter(func.lower(Novel.author.name).like(f"%{payload.author.lower()}%"))
    
    if payload.chaptersOption == "max":
        query = query.filter(Novel.chapters <= payload.chapters)
    elif payload.chaptersOption == "min":
        query = query.filter(Novel.chapters >= payload.chapters)
    
    if payload.ratingOption == "max":
        query = query.filter(Novel.rating <= payload.rating)
    elif payload.ratingOption == "min":
        query = query.filter(Novel.rating >= payload.rating)
    
    if payload.reviewsOption == "max":
        query = query.filter(Novel.reviews <= payload.reviews)
    elif payload.reviewsOption == "min":
        query = query.filter(Novel.reviews >= payload.reviews)
    
    if payload.viewOption == "max":
        query = query.filter(Novel.view_count <= payload.view)
    elif payload.viewOption == "min":
        query = query.filter(Novel.view_count >= payload.view)
    
    if payload.genreInclude:
        query = query.filter(Novel.genres.any(func.lower(Novel.genres).in_([g.lower() for g in payload.genreInclude])))
    
    if payload.genreExclude:
        query = query.filter(~Novel.genres.any(func.lower(Novel.genres).in_([g.lower() for g in payload.genreExclude])))
    
    if payload.tagsInclude:
        query = query.filter(Novel.tags.any(func.lower(Novel.tags).in_([t.lower() for t in payload.tagsInclude])))
    
    if payload.tagsExclude:
        query = query.filter(~Novel.tags.any(func.lower(Novel.tags).in_([t.lower() for t in payload.tagsExclude])))

    # Sorting based on sortBy criteria
    sort_column = None
    if payload.sortBy.lower() == "rating":
        sort_column = Novel.rating
    elif payload.sortBy.lower() == "review":
        sort_column = Novel.reviews
    elif payload.sortBy.lower() == "view":
        sort_column = Novel.view_count
    elif payload.sortBy.lower() == "chapters":
        sort_column = Novel.chapters
    elif payload.sortBy.lower() == "newest":
        sort_column = Novel.created_date
    
    if sort_column:
        if payload.isAscending:
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

    novels = query.all()
    return novels

def follow(db: Session, payload: FollowPayload):
    user = db.query(User).filter(User.id == int(payload.userId)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    target_user = db.query(User).filter(User.id == int(payload.followId)).first()
    if target_user is None:
        raise HTTPException(status_code=404, detail="Target user not found")
    
    # if user.following is None:
    #     user.following = [target_user.id]
    # else:
    #     user.following.append(target_user.id)
    
    # if target_user.followers is None:
    #     target_user.followers = [user.id]
    # else: 
    #     target_user.followers.append(user.id)
    following_temp = []
    if user.following is not None:
        if target_user.id not in user.following:
            for following in user.following:
                following_temp.append(following)
            following_temp.append(target_user.id)    
    else:    
        following_temp.append(target_user.id)
    user.following = following_temp
    
    followers_temp = []
    if target_user.followers is not None:
        if user.id not in target_user.followers:
            for follower in target_user.followers:
                followers_temp.append(follower)
            followers_temp.append(user.id)
        else:
            followers_temp.append(user.id)
    target_user.followers = followers_temp

    try:
        db.commit()
        db.refresh(user)
        db.refresh(target_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update follow relationship") from e
    
    return target_user

def unfollow(db: Session, payload: FollowPayload):
    user_id = int(payload.userId)
    follow_id = int(payload.followId)
    
    # Fetch user and target_user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    target_user = db.query(User).filter(User.id == follow_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Target user not found")
    
    # Remove target_user's ID from user's following array
    if target_user.id in user.following:
        user.following.remove(target_user.id)
    
    # Remove user's ID from target_user's followers array
    if user.id in target_user.followers:
        target_user.followers.remove(user.id)
    
    try:
        db.commit()
        db.refresh(user)
        db.refresh(target_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update follow relationship") from e
    
    return target_user

def get_library_list(db: Session, user_id: str):
    libraries = db.query(Library).filter(Library.user_id == int(user_id)).all()
    if not libraries:
        raise HTTPException(status_code=404, detail="Library not found")
    return libraries

def remove_novel_from_list(db: Session, payload: RemoveNovelFromListPayload):
    library = db.query(Library).filter(Library.id == int(payload.listId)).first()
    if library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    if library.user_id != int(payload.userId):
        raise HTTPException(status_code=403, detail="Unauthorized access")
    if int(payload.novelId) not in library.novels:
        raise HTTPException(status_code=404, detail="Novel not found in list")
    library.novels.remove(int(payload.novelId))
    db.commit()
    return {"message": "Novel removed from list"}

def create_novel_list(db: Session, payload: CreateListPayload):
    user = db.query(User).filter(User.id == int(payload.userId)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_library = Library(
        user_id=int(payload.userId),
        title=payload.title or "Untitled",
        is_public=payload.isPublic or True,
        novels=[]
    )
    db.add(db_library)
    db.commit()
    db.refresh(db_library)
    return db_library

def add_novel_to_list(db: Session, payload: AddNovelToListPayload):
    library = db.query(Library).filter(Library.id == int(payload.listId)).first()
    if library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    if library.user_id != int(payload.userId):
        raise HTTPException(status_code=403, detail="Unauthorized access")
    if int(payload.novelId) in library.novels:
        raise HTTPException(status_code=404, detail="Novel already in list")
    library.novels.append(int(payload.novelId))
    db.commit()
    db.refresh(library)
    return library

def delete_library_list(db: Session, payload: DeleteLibraryListPayload):
    library = db.query(Library).filter(Library.id == int(payload.listId)).first()
    if library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    if library.user_id != int(payload.userId):
        raise HTTPException(status_code=403, detail="Unauthorized access")
    db.delete(library)
    db.commit()
    return library

def update_library_list_privacy(db: Session, payload: UpdateLibraryListPrivacyPayload):
    library = db.query(Library).filter(Library.id == int(payload.listId)).first()
    if library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    if library.user_id != int(payload.userId):
        raise HTTPException(status_code=403, detail="Unauthorized access")
    library.is_public = payload.isPublic
    db.commit()
    db.refresh(library)
    return library

def update_library_list_title(db: Session, payload: UpdateLibraryListTitlePayload):
    library = db.query(Library).filter(Library.id == int(payload.listId)).first()
    if library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    if library.user_id != int(payload.userId):
        raise HTTPException(status_code=403, detail="Unauthorized access")
    library.title = payload.title
    db.commit()
    db.refresh(library)
    return library

def get_view_per_genre(db: Session):
    genres = db.query(Genre).all()
    genre_views = []
    for genre in genres:
        novels = db.query(Novel).filter(Novel.genres.contains(genre.name)).all()
        view_count = sum(novel.view_count for novel in novels)
        genre_views.append({
            "genre": genre.name,
            "viewCount": view_count
        })
    return genre_views

def get_view_per_tag(db: Session):
    tags = db.query(Tag).all()
    tag_views = []
    for tag in tags:
        novels = db.query(Novel).filter(Novel.tags.contains(tag.name)).all()
        view_count = sum(novel.view_count for novel in novels)
        tag_views.append({
            "tag": tag.name,
            "viewCount": view_count
        })
    return tag_views

def get_view_per_novel(db: Session, payload: ViewPerNovelPayload):
    novels = db.query(Novel).filter(Novel.author_id == payload.authorId).all()
    novel_views = []
    for novel in novels:
        novel_views.append({
            "novelId": novel.id,
            "novelName": novel.title,
            "viewCount": novel.view_count
        })
    return novel_views

def get_review_per_novel(db: Session, payload: ViewPerNovelPayload):
    novels = db.query(Novel).filter(Novel.author_id == payload.authorId).all()
    novel_reviews = []
    for novel in novels:
        reviews = db.query(Review).filter(Review.novel_id == novel.id).all()
        review_count = len(reviews)
        novel_reviews.append({
            "novelId": novel.id,
            "novelName": novel.title,
            "reviewCount": review_count
        })
    return novel_reviews

def get_comment_per_chapter(db: Session, payload: CommentPerChapterPayload):
    chapters = db.query(Chapter).filter(Chapter.novel_id == payload.novelId).all()
    chapter_comments = []
    for chapter in chapters:
        comments = db.query(Comment).filter(Comment.chapter_id == chapter.id).all()
        comment_count = len(comments)
        chapter_comments.append({
            "chapterTitle": chapter.title,
            "commentCount": comment_count
        })
    return chapter_comments

def get_user_per_time(db: Session, payload: UserPerTimePayload) -> UserPerTime:
    year = int(payload.year)
    
    query = db.query(
        extract('month', User.created_date).label('month'),
        func.count(User.id).label('count')
    ).filter(
        extract('year', User.created_date) == year
    ).group_by(
        extract('month', User.created_date)
    ).order_by(
        extract('month', User.created_date)
    )
    
    # If isNewAccount is True, filter only new accounts
    if payload.isNewAccount:
        query = query.filter(User.is_new_account == True)
    
    results = query.all()

    # Initialize user counts with zeroes for each month
    user_counts = [0] * 12

    # Populate user counts from the query results
    for result in results:
        month_index = int(result.month) - 1  # Month is 1-based, list is 0-based
        user_counts[month_index] = result.count

    return UserPerTime(userCount=user_counts)

def get_original_works(db: Session, user_id: str):
    novels = db.query(Novel).filter(Novel.author_id == int(user_id)).all()
    original_works = []
    for novel in novels:
        if novel.author_id:
            original_works.append(novel)
    return original_works