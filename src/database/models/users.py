from sqlalchemy import Column, Integer, String, DateTime, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.dependencies import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    name = Column(String)
    hashed_password = Column(String)
    followers = Column(ARRAY(Integer))
    following = Column(ARRAY(Integer))
    avatar = Column(String)
    admin_type = Column(Integer)
    created_date = Column(DateTime(timezone=True))

    novels = relationship("Novel", back_populates="author", cascade="all, delete", passive_deletes=True)
    comments = relationship("Comment", back_populates="user", cascade="all, delete", passive_deletes=True)
    reports = relationship("Report", back_populates="user" , cascade="all, delete", passive_deletes=True)
    reviews = relationship("Review", back_populates="user", cascade="all, delete", passive_deletes=True)
    library = relationship("Library", back_populates="user", cascade="all, delete", passive_deletes=True)