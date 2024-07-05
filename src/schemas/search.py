from pydantic import BaseModel, ConfigDict
from datetime import datetime

class SearchNovelPayload(BaseModel):
    title: str
    author: str
    chapters: int # number of chapters
    chaptersOption: str # max / min
    rating: float
    ratingOption: str # max / min
    reviews: int # number of reviews
    reviewsOption: str # max / min
    view: int # number of views
    viewOption: str # max / min
    genreInclude: list[str]
    genreExclude: list[str]
    tagsInclude: list[str]
    tagsExclude: list[str]
    sortBy: str #  Rating, review, view, chapters, newest
    isAscending: bool # true / false (for sortBy option)

