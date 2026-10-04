import jwt
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from ...api.deps import current_user
from ...core.config import settings
from ...core.database import get_db
from ...models import AudioAsset, Chapter, Book, User
from ...services.storage import storage
router = APIRouter(prefix="/assets", tags=["assets"])
@router.get("/audio/{asset_id}")
def audio(asset_id: int, request: Request, token: str | None = Query(default=None), db: Session = Depends(get_db)):
    raw_token = token or request.headers.get("Authorization", "").removeprefix("Bearer ")
    try: user = db.get(User, int(jwt.decode(raw_token, settings.jwt_secret, algorithms=["HS256"])["sub"]))
    except (jwt.PyJWTError, KeyError, ValueError): user = None
    if not user: raise HTTPException(401, "Authentication required")
    asset = db.scalar(select(AudioAsset).join(Chapter).join(Book).where(AudioAsset.id == asset_id, Book.user_id == user.id))
    if not asset: raise HTTPException(404, "Audio not found")
    return Response(storage.read(asset.storage_key), media_type=asset.mime_type, headers={"Accept-Ranges": "bytes"})
