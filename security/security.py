import bcrypt
import jwt
from jwt import PyJWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from database.database import get_db
from database.model import Users
from sqlalchemy.orm import Session
from env_loader import SECREATKEY, ALGORITHM



security_key = SECREATKEY
algorithm = ALGORITHM
security_scheme = HTTPBearer()

def hash_password(plain_password : str) -> str:
    raw_pswd = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(raw_pswd, salt)
    return hashed_password.decode("utf-8")

def verify_password(plain_password : str, hashed_password : str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(user_id : int, email : str, exp : int = 10):
    try:
        exp_time = datetime.now(timezone.utc) + timedelta(days=exp)
        payload = {
            "user_id" : user_id,
            "email" : email,
            "exp" : int(exp_time.timestamp())
        }
        return jwt.encode(payload, security_key, algorithm)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token or signature"
        )

def check_access_token(credentials : HTTPAuthorizationCredentials = Depends(security_scheme), db : Session = Depends(get_db)):
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid token or expired",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        details = jwt.decode(token, security_key, algorithms=[algorithm])
        user_id = details.get("user_id")
        if not user_id:
            raise credentials_exception
        check_user = db.query(Users).filter(Users.id == user_id).first()
        if not check_user:
            raise credentials_exception
    except PyJWTError:
        return credentials_exception
    return check_user
