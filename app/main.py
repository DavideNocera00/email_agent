from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserOut, UserCreate
from app import crud

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "OK, the server is running!"}

@app.post("/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users", response_model=list[UserOut])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)