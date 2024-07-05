from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ReviewFullInfo(BaseModel):
    id: str
    userId: str
    novelId: str
    review: str # content (review text) of the review
    rating: int
    liked: list[str] # list of user ids who liked the review
    createAt: str
    novelTitle: str
    userAvatar: str
    userName: str
    updateDate: str