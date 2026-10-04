import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..core.config import settings
from ..core.database import get_db
from ..models import User

bearer = HTTPBearer(auto_error=False)
def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db: Session = Depends(get_db)) -> User:
    if not credentials: raise HTTPException(401, "Authentication required")
    try: user_id = int(jwt.decode(credentials.credentials, settings.jwt_secret, algorithms=["HS256"])["sub"])
    except (jwt.PyJWTError, KeyError, ValueError): raise HTTPException(401, "Invalid or expired token")
    user = db.scalar(select(User).where(User.id == user_id))
    if not user: raise HTTPException(401, "User not found")
    return user
