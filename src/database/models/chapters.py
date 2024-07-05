from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.database.dependencies import Base


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    novel_id = Column(Integer, ForeignKey("novels.id", ondelete="CASCADE"))
    title = Column(String)
    content = Column(String)
    status = Column(String)
    chapter = Column(Integer)
    view_count = Column(Integer)
    created_date = Column(DateTime(timezone=True))

    novel = relationship("Novel", back_populates="chapters")
    comments = relationship("Comment", back_populates="chapter", cascade="all, delete", passive_deletes=True)
