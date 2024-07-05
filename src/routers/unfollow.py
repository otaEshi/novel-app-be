from fastapi import APIRouter
from src.database.dependencies import DBSession
from src import crud
from src.schemas.user import FollowPayload

router = APIRouter()

@router.patch("/")
def unfollow_request(db: DBSession, payload: FollowPayload):
    crud.unfollow(db, payload)

    return {"message": "Unfollow successful"}