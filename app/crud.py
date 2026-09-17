from sqlalchemy.orm import Session

from app.schemas import UserCreate
from app.models import User, EmailDigest, DigestItem

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

def save_digest(db: Session, user_id: int, digest_text: str, items: list[dict]) -> EmailDigest:
    digest = EmailDigest(user_id = user_id, digest_text = digest_text)
    db.add(digest)
    db.flush()

    for item in items:
        digest_item = DigestItem(
            digest_id=digest.id,
            sender=item.get("sender"),
            subject=item.get("subject"),
            summary=item["summary"],
            category=item.get("category"),
            requires_action=item.get("requires_action", False),
        )

        db.add(digest_item)

    db.commit()
    db.refresh(digest)
    return digest