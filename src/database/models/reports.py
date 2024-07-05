from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.database.dependencies import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    target_id = Column(Integer)
    report_type = Column(String) # report type novel, warning, chapter!, comment!, review!
    reason = Column(String)
    processed = Column(Boolean)

    user = relationship("User", back_populates="reports")