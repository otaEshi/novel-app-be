from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, ARRAY, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.dependencies import Base


class Novel(Base):
    __tablename__ = "novels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String)
    image = Column(String)
    genres = Column(ARRAY(String)) # genres name
    tags = Column(ARRAY(String))    # tags name
    view_count = Column(Integer)
    description = Column(String)
    last_chapter_created_date = Column(DateTime(timezone=True))
    created_date = Column(DateTime(timezone=True))
    is_warning = Column(Boolean)
    status = Column(String)

    author = relationship("User", back_populates="novels")
    chapters = relationship("Chapter", back_populates="novel", cascade="all, delete", passive_deletes=True)
    reviews = relationship("Review", back_populates="novel", cascade="all, delete", passive_deletes=True)