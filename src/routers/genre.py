from src.database.dependencies import DBSession
from fastapi import APIRouter, Depends, HTTPException, status
from src import crud

router = APIRouter()

@router.get("/genre-list")
def get_genre_list(db: DBSession):
    genres = crud.get_genre_list(db)
    return genres