from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_or_update_user(db: Session, email: str, refresh_token: str) -> User:
    user = get_user_by_email(db, email)
    if user:
        user.google_refresh_token = refresh_token
    else:
        user = User(email=email, google_refresh_token=refresh_token)
        db.add(user)
    db.commit()
    db.refresh(user)
    return user