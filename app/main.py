from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserOut, UserCreate
from app import crud
from app.auth.oauth import get_authorization_url, exchange_code_for_tokens, get_user_email

app = FastAPI(title="Email Agent API")

#Temporary in-memory storage for OAuth state (only for development purposes)

oauth_states = {}

@app.get("/health")
def health_check():
    return {"status": "OK, the server is running!"}

@app.post("/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users", response_model=list[UserOut])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.get("/auth/login")
def login():
    authorization_url, state, code_verifier = get_authorization_url()
    oauth_states[state] = code_verifier  # salviamo anche il code_verifier, non solo True
    return RedirectResponse(authorization_url)


@app.get("/auth/callback")
def callback(code: str, state: str, db: Session = Depends(get_db)):
    if state not in oauth_states:
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    code_verifier = oauth_states.pop(state)
    tokens = exchange_code_for_tokens(code, code_verifier)

    email = get_user_email(tokens["access_token"])
    user = crud.create_or_update_user(db, email=email, refresh_token=tokens["refresh_token"])

    return {"message": "Login successful", "user_email": user.email, "user_id": user.id}