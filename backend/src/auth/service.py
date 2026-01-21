import jwt
from jwt import PyJWTError
from typing import Dict, Any
from datetime import timedelta, datetime, timezone
from uuid import UUID
from passlib.context import CryptContext
from src.core.entities import User

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)

def authenticate_user(username: str, password: str, db) -> User | None:
    user = db.query(User).filter(User.email == username).first()

    # If the user does not exist or the password is incorrect, return None
    if not user or not verify_password(password, user.password_hash): 
        return None
    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

def create_token(user_id: UUID, token_version: int, expiry: timedelta, SECRET_KEY: str, ALGORITHM: str, refresh: bool):
    if refresh:
        token_type = "refresh"
    else:
        token_type = "access"

    encode = {
        "sub": str(user_id),
        "token_version": token_version,
        "type": token_type,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + expiry,
    }

    return jwt.encode(payload=encode, key=SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, SECRET_KEY: str, ALGORITHM: str, refresh: bool) -> Dict[str, Any] | None:
    if refresh:
        token_type = "refresh"
    else:
        token_type = "access"  
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != token_type:
            return None
        return payload
    except PyJWTError as e:
        return None