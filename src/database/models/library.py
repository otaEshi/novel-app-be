from sqlalchemy import Column, String, Boolean, ARRAY, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.database.dependencies import Base


class Library(Base):
    __tablename__ = "library"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String)
    is_public = Column(Boolean)
    novels = Column(ARRAY(Integer))

    user = relationship("User", back_populates="library")