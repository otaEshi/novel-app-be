from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from pydantic import BaseModel

from typing import List, Optional

from src.crud import create_user
from src.database.dependencies import DBSession
from src.database.models.users import User
from src.schemas.user import UserBase, UserInput, UserCreate
from src.security import validate_token
from src.schemas.schemas import User as UserSchema, Novel as NovelSchema, Review as ReviewSchema, Report as ReportSchema

router = APIRouter()

class UpdateUserProfileRequest(BaseModel):
    name: str
    avatar: Optional[str]

class GetReportRequest(BaseModel):
    id: int
    user_id: int
    report_type: str

@router.post("/")
async def create_user_api(
    user_in: UserCreate,
    db_session: DBSession,
) -> str:
    try:
        user_created = create_user(db_session, user_in)
        if user_created:
            return "User creation successful"
    except Exception as e:
        raise e


# @router.get("/", response_model=list[UserBase],)
# async def get_users(
#     db_session: DBSession,
# ) -> list[UserBase]:
#     all_users = db_session.execute(select(User)).scalars().all()
#     if not all_users:
#         raise HTTPException(status_code=404, detail="No users found")
#     return [UserBase.model_validate(user) for user in all_users]

# @router.get("/{user_id}", response_model=UserSchema)
# async def get_user(user_id: str, db: DBSession ):
#     user = get_user(user_id, db)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# @router.get("/original-works/{user_id}", response_model=List[NovelSchema])
#  return list of novel

# async def get_original_works(user_id: int, db: DBSession = Depends(get_db)):
#     novels = db.query(Novel).filter(Novel.author_id == user_id).all()
#     return novels

# @router.get("/reviews/{user_id}", response_model=List[ReviewSchema])
#  return list of reviews

# async def get_user_reviews(user_id: int, db: DBSession = Depends(get_db)):
#     reviews = db.query(Review).filter(Review.user_id == user_id).all()
#     return reviews

# @router.patch("/", response_model=UserSchema)
# async def update_user_profile(payload: UpdateUserProfileRequest, db: DBSession):
#     user = db.query(User).filter(User.id == payload.id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     user.name = payload.name
#     if payload.avatar:
#         user.avatar = payload.avatar
#     db.commit()
#     db.refresh(user)
#     return user

# @router.get("/report", response_model=ReportSchema)
# async def get_report(payload: GetReportRequest, db: DBSession = Depends(get_db)):
#     report = db.query(Report).filter(Report.id == payload.id, Report.user_id == payload.user_id, Report.report_type == payload.report_type).first()
#     if not report:
#         raise HTTPException(status_code=404, detail="Report not found")
#     return report