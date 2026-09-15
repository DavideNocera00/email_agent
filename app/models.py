from sqlalchemy import Column, Integer, String
from app.database import Base

# Define the User model which represent the table into the database
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    google_refresh_token = Column(String, nullable=True)