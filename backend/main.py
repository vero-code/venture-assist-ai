# backend/main.py
import os
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import google.auth.transport.requests
from google_auth_oauthlib.flow import Flow

load_dotenv()

app = FastAPI()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")

# The scopes (SCOPES) your application requests access to
# drive.file - for Google Drive
SCOPES = [
    "https://www.googleapis.com/auth/drive.file"
]

# There will be a database in production
# key: user_id (or session_id), value: dict with tokens
user_tokens_store = {}

@app.get("/")
async def read_root():
    return {"message": "Venture Assist AI Backend is running!"}

@app.get("/auth/google")
async def google_auth():
    """
    Initiates Google's OAuth flow.
    Redirects the user to Google's consent page.
    """
    if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI]):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google API credentials are not set in environment variables."
        )

    # Create a Flow object to run the OAuth flow
    # client_secrets_file is not used here because gets the ID and SECRET from .env
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "project_id": GOOGLE_PROJECT_ID,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uris": [GOOGLE_REDIRECT_URI]
            }
        },
        scopes=SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI
    )

    # Generate URL for authorization
    authorization_url, state = flow.authorization_url(
        access_type='offline',  # Request refresh token
        include_granted_scopes='true'
    )

    # For production apps, the state parameter must be saved in the user's session and validated upon return from /oauth2callback to prevent CSRF attacks.

    return RedirectResponse(authorization_url)