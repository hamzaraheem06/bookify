from fastapi import APIRouter
from .routes import auth, books, progress, assets, library, search
api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)
api_router.include_router(books.router)
api_router.include_router(progress.router)
api_router.include_router(assets.router)
api_router.include_router(library.router)
api_router.include_router(search.router)
