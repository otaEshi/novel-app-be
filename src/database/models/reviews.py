from sqlalchemy import Column, Integer, String, Date, ForeignKey, ARRAY, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.dependencies import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    novel_id = Column(Integer, ForeignKey("novels.id", ondelete="CASCADE"))
    content = Column(String)
    rating = Column(Integer)
    liked = Column(ARRAY(Integer))
    created_date= Column(DateTime(timezone=True))
    updated_date= Column(DateTime(timezone=True))

    user = relationship("User", back_populates="reviews")
    novel = relationship("Novel", back_populates="reviews")