from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

# Define the User model which represent the table into the database
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    google_refresh_token = Column(String, nullable=True)

    digest = relationship("EmailDigest", back_populates="user")

class EmailDigest(Base):
    __tablename__ = "email_digest"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    digest_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user =relationship("User", back_populates="digest")
    items = relationship("DigestItem", back_populates="digest")

class DigestItem(Base):
    __tablename__ = "digest_item"

    id = Column(Integer, primary_key=True, index=True)
    digest_id = Column(Integer, ForeignKey("email_digest.id"), nullable=False)
    sender = Column(String, nullable=True)
    subject = Column(String, nullable=True)
    summary = Column(Text, nullable=False)
    category = Column(String, nullable=True)
    requires_action = Column(Boolean, nullable=True)

    digest = relationship("EmailDigest", back_populates="items")