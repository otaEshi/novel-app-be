from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.dependencies import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    chapter_id = Column(Integer, ForeignKey("chapters.id", ondelete="CASCADE"))
    content = Column(String)
    liked = Column(ARRAY(Integer))
    created_date= Column(DateTime(timezone=True))

    user = relationship("User", back_populates="comments")
    chapter = relationship("Chapter", back_populates="comments")