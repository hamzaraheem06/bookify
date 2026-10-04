from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from ...api.deps import current_user
from ...core.database import get_db
from ...models import User
from ...services.auth import authenticate, create_token, hash_password
router = APIRouter(prefix="/auth", tags=["auth"])
class Credentials(BaseModel):
    email: EmailStr; password: str = Field(min_length=8); display_name: str = Field(default="BookPilot listener", min_length=1, max_length=120)
class AuthOut(BaseModel): token: str; user_id: int; email: str; display_name: str
@router.post("/register", response_model=AuthOut, status_code=201)
def register(payload: Credentials, db: Session = Depends(get_db)):
    email = str(payload.email).lower()
    if db.scalar(select(User).where(User.email == email)): raise HTTPException(409, "An account with that email already exists")
    user = User(email=email, password_hash=hash_password(payload.password), display_name=payload.display_name); db.add(user); db.commit(); db.refresh(user)
    return AuthOut(token=create_token(user), user_id=user.id, email=user.email, display_name=user.display_name)
@router.post("/login", response_model=AuthOut)
def login(payload: Credentials, db: Session = Depends(get_db)):
    user = authenticate(db, str(payload.email), payload.password)
    if not user: raise HTTPException(401, "Invalid email or password")
    return AuthOut(token=create_token(user), user_id=user.id, email=user.email, display_name=user.display_name)
@router.get("/me", response_model=AuthOut)
def me(user: User = Depends(current_user)): return AuthOut(token="", user_id=user.id, email=user.email, display_name=user.display_name)
