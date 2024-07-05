from pydantic import BaseModel
from datetime import datetime

class SearchUserPayload(BaseModel):
    username: str

class AdjustAccountRightPayload(BaseModel):
    userId: str # target user's id
    admin_type: str # admin_type change to of the user
    currentuserId: str # admin id to check authorization

class AdminHandleReportPayload(BaseModel):
    userId: str
    reportId: str
    processed: bool