import hashlib, hmac, secrets
from datetime import datetime, timedelta, timezone
import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..core.config import settings
from ..models import User

def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120_000)
    return f"pbkdf2_sha256$120000${salt.hex()}${digest.hex()}"

def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, rounds, salt, digest = encoded.split("$")
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), int(rounds)).hex()
        return algorithm == "pbkdf2_sha256" and hmac.compare_digest(actual, digest)
    except (ValueError, TypeError):
        return False

def create_token(user: User) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": str(user.id), "exp": now + timedelta(minutes=settings.jwt_expire_minutes)}, settings.jwt_secret, algorithm="HS256")

def authenticate(db: Session, email: str, password: str) -> User | None:
    user = db.scalar(select(User).where(User.email == email.lower().strip()))
    return user if user and verify_password(password, user.password_hash) else None
