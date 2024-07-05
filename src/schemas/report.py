from pydantic import BaseModel
from src.schemas.review import ReviewFullInfo
from src.schemas.comment import CommentFullInfo

class BaseReport (BaseModel):
    reportId: str
    userId: str
    reason: str
    processed: bool

class ReportWarningFullInfoResponse (BaseReport):
    adminId: str

class ReportNovelFullInfoResponse (BaseReport):
    novelId: str

class ReportReviewFullInfoResponse (BaseReport):
    reviewId: str
    review: ReviewFullInfo

class ReportCommentFullInfoResponse (BaseReport):
    commentId: str
    comment: CommentFullInfo

class ReportChapterFullInfoResponse (BaseReport):
    chapterId: str
    chapterTitle: str

class AdminReportList (BaseModel):
    reportReview: list[ReportReviewFullInfoResponse]
    reportNovel: list[ReportNovelFullInfoResponse]
    reportComment: list[ReportCommentFullInfoResponse]

class SendWarningPayload (BaseModel):
    adminId: str
    userId: str
    novelId: str
    reason: str
    processed: bool