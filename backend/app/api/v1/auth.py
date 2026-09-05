from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, User
from app.services.auth_service import create_user, authenticate_user
from app.core.security import create_access_token

router = APIRouter()

@router.post("/register", response_model=User, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user_data)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}