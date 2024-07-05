# import db models, so alembic migration can detect it
from src.database.models.users import User  
from src.database.models.novels import Novel 
from src.database.models.reports import Report
from src.database.models.reviews import Review
from src.database.models.comments import Comment
from src.database.models.chapters import Chapter
from src.database.models.library import Library
from src.database.models.genres import Genre
from src.database.models.tags import Tag