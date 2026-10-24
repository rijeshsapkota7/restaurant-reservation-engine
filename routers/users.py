from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from database.database import get_db
from pydantic import BaseModel
from typing import Literal
from sqlalchemy.orm import Session
from database.model import Users
from security.security import hash_password, verify_password, check_access_token, create_access_token

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreate(BaseModel):
    name : str
    email : str
    password : str
    role : Literal["customer", "owner"]

class UserLogin(BaseModel):
    email : str
    password : str

@router.post("/register", status_code=201)
def create_user(data : UserCreate, db : Session = Depends(get_db)):
    chec_duplication = db.query(Users).filter(Users.email == data.email).first()
    if chec_duplication:
        raise HTTPException(status_code=409, detail="User with email already exist")
    hashed_password = hash_password(data.password)
    new_user = Users(name=data.name, email=data.email, password=hashed_password, role=data.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"Message" : "User created successfully", "details" : new_user}

@router.post("/login")
def login_user(data : UserLogin, db : Session = Depends(get_db)):
    check_user_db = db.query(Users).filter(Users.email == data.email).first()
    user_exception = HTTPException(status_code=401, detail="Email or Password is incorrect")
    if not check_user_db:
        raise user_exception
    if verify_password(data.password, check_user_db.password):
        access_token = create_access_token(check_user_db.id, data.email)
        return {"token" : access_token, "type" : "bearer"}
    else:
        raise user_exception
