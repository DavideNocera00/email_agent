from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# Create the SQLAlchemy engine which configure the database connection
engine = create_engine(DATABASE_URL)

# Create a new instance of a sessionmaker, which will be used to create new sessions for interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class. Our future models will inherit from this class.
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()