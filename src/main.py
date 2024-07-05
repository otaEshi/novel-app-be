from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.routers import dashboard, library, follow, unfollow, search, token, admin, user, auth, novel, genre, tag
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="novel-app-backend",
    description="novel-app-backend"
)
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=['*'],
    allow_methods=['*'],
)

    # safe
app.include_router(token.router, prefix="/token", tags=["token"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(novel.router, prefix="/novel", tags=["novel"])
app.include_router(tag.router, prefix="/tags", tags=["tags"])
app.include_router(genre.router, prefix="/genre", tags=["genre"])
app.include_router(follow.router, prefix="/follow", tags=["follow"])
app.include_router(unfollow.router, prefix="/unfollow", tags=["unfollow"])
app.include_router(library.router, prefix="/library", tags=["library"])

    # bug attributeError media_type
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(search.router, prefix="/search", tags=["search"])
