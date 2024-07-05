from pydantic import BaseModel

class CommentFullInfo (BaseModel):
    commentId: str
    userId: str
    name: str
    avatar: str
    content: str
    novelId: str
    chapterId: str
    createDate: str
    liked: list[str] # Array of user IDs who liked the comment

class DeleteCommentPayload(BaseModel):
    userId: str
    commentId: str