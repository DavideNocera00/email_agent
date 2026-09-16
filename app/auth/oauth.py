from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest

from app.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, GOOGLE_SCOPES

import requests


def get_flow(code_verifier: str | None = None) -> Flow:
    client_config = {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [GOOGLE_REDIRECT_URI],
        }
    }
    flow = Flow.from_client_config(
        client_config,
        scopes=GOOGLE_SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI,
    )
    if code_verifier:
        flow.code_verifier = code_verifier
    return flow


def get_authorization_url() -> tuple[str, str, str]:
    flow = get_flow()
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    return authorization_url, state, flow.code_verifier


def exchange_code_for_tokens(code: str, code_verifier: str) -> dict:
    flow = get_flow(code_verifier=code_verifier)
    flow.fetch_token(code=code)
    credentials = flow.credentials
    return {
        "access_token": credentials.token,
        "refresh_token": credentials.refresh_token,
    }

#Retrieve the user's email using the access token
def get_user_email(access_token: str) -> str:
    response = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()
    return response.json()["email"]

# We build a Credentials object with the refresh token and we contact Google's token endpoint using the client_ID and client_secret.
# The function return the new access_token that can be used to access the user's Gmail data.
def get_valid_access_token(refresh_token: str) -> str:
    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
    )
    credentials.refresh(GoogleRequest())
    return credentials.token