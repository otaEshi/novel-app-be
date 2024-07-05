from fastapi import APIRouter
from src.database.dependencies import DBSession
from src import crud
from src.schemas.user import FollowPayload, FollowReponse

router = APIRouter()
@router.patch("/")
def follow_request(db: DBSession, payload: FollowPayload):
    user = crud.follow(db, payload)

    return_user = FollowReponse(
        id= str(user.id),
        name= user.name,
        avatar= user.avatar or ""
    )

    return return_user