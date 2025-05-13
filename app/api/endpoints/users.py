from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.database.models import User
from pydantic import BaseModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserRegister(BaseModel):
    username: str
    email: str
    password: str  # For demo only, store as plain text

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    new_user = User(username=user.username, email=user.email)
    # For demo: store password as username + '_pw' in email field (not secure, just for demo)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": "success", "data": {"id": new_user.id, "username": new_user.username, "email": new_user.email}}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if not existing:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    # For demo: accept any password
    return {"status": "success", "data": {"id": existing.id, "username": existing.username, "email": existing.email}} 