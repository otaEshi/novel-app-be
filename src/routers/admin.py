from src.database.dependencies import DBSession
from fastapi import APIRouter, Depends, HTTPException, status
from src import crud
from src.routers.user import get_user
from src.schemas.admin import AdminHandleReportPayload, SearchUserPayload, AdjustAccountRightPayload
from src.schemas.report import SendWarningPayload, AdminReportList, ReportNovelFullInfoResponse, ReportReviewFullInfoResponse, ReportCommentFullInfoResponse
from src.routers.user import get_user_review, get_comment_for_report
from src.schemas.comment import DeleteCommentPayload

router = APIRouter()

@router.get("/get-admin-list")
def get_admin_list(db: DBSession):
    admins = crud.get_admin_list(db)

    admin_list = []

    for admin in admins:
        admin = get_user(admin.id, db)
        admin_list.append(admin)

    return admin_list

@router.get("/search-user")
def admin_search_user(db: DBSession, payload: SearchUserPayload):
    users = crud.get_users(db, 0, payload.username)

    user_list = []
    for user in users:
        user = get_user(user.id, db)
        user_list.append(user)

    return user_list

@router.patch("/right")
def adjust_admin_right(db: DBSession, payload: AdjustAccountRightPayload):
    target_user = crud.adjust_admin_right(db, payload.currentuserId)

    return_user = get_user(target_user.id, db)
    return return_user

@router.get("/report")
def get_admin_report_list(db: DBSession):
    reports = crud.get_report_for_admin(db)

    if not reports:
        raise HTTPException(status_code=404, detail="No reports found")

    reportReview = []
    reportNovel = []
    reportComment = []

    for report in reports:
        if report.type != type:
            continue
        
        if type == "novel":
            return_report = ReportNovelFullInfoResponse(
                reportId=str(report.id),
                userId=str(report.user_id),
                novelId=str(report.target_id),
                reason=report.reason,
                processed=report.processed
            )
            reportNovel.append(return_report)
        elif type == "review":
            review = get_user_review(report.user_id, db)
            if not review:
                raise HTTPException(status_code=404, detail="Review not found")
            return_report = ReportReviewFullInfoResponse(
                reportId=str(report.id),
                userId=str(report.user_id),
                reviewId=str(report.target_id),
                review=review,
                reason=report.reason,
                processed=report.processed
            )
            reportReview.append(return_report)
        elif type == "comment":
            comment = get_comment_for_report(report.target_id, db)
            if not comment:
                raise HTTPException(status_code=404, detail="Comment not found")
            return_report = ReportCommentFullInfoResponse(
                reportId=str(report.id),
                userId=str(report.user_id),
                commentId=str(report.target_id),
                comment=comment,
                reason=report.reason,
                processed=report.processed
            )
            reportReview.append(return_report)

    return_report = AdminReportList(
        reportReview=reportReview,
        reportNovel=reportNovel,
        reportComment=reportComment
    )

    if not return_report:
        raise HTTPException(status_code=404, detail=f"No reports found")

    return return_report

@router.post("/send-warning")
def send_warning(db: DBSession, payload: SendWarningPayload):
    crud.send_warning(db, payload)
    return {"message": "Warning sent"}

@router.patch("handle-report")
def handle_report(db: DBSession, payload: AdminHandleReportPayload):
    crud.handle_report(db, payload)
    return {"message": "Report handled"}

@router.delete("/comment")
def delete_comment(db: DBSession, payload: DeleteCommentPayload):
    crud.delete_comment(db, payload)
    return {"message": "Comment deleted"}