from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import UserCreate
from app.models import User
from app.database import get_db
from app.auth import generate_email_token, verify_email_token
from app.mailer import send_verification_email
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register/")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    hashed_password = pwd_context.hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password, full_name=user.full_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = generate_email_token(new_user.email)
    await send_verification_email(new_user.email, token)

    return {"message": "Регистрация успешна. Подтвердите email."}

@router.get("/verify")
def verify_email(token: str, db: Session = Depends(get_db)):
    email = verify_email_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Неверный или просроченный токен")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user.is_verified = True
    db.commit()
    return {"message": "Email подтверждён успешно!"}
