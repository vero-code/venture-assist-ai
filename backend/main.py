# backend/main.py
import os
from fastapi import FastAPI, HTTPException, status, Request
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

if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, GOOGLE_PROJECT_ID]):
    raise ValueError("Google API credentials are not set in environment variables. Please check your .env file.")

FRONTEND_URL = os.getenv("FRONTEND_URL")

if not FRONTEND_URL:
    raise ValueError("FRONTEND_URL is not set in environment variables. Please check your .env file.")

# TDefine Google API scopes required by the application.
SCOPES = [
    "https://www.googleapis.com/auth/drive.file"
]

# In-memory store for user tokens (for MVP/hackathon demo).
# In production, this would be a persistent database (e.g., PostgreSQL, Redis)
# mapping user_id to their Google tokens.
user_tokens_store = {}

# Placeholder user ID for the MVP/hackathon.
# In a real application, this would come from a user authentication system.
TEST_USER_ID = "some_unique_user_id_for_testing"

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

    authorization_url, state = flow.authorization_url(
        access_type='offline',  # Request a refresh token for long-term access
        include_granted_scopes='true'
    )

    # Note: For production, the 'state' parameter must be saved in the user's session
    # and validated upon return from /oauth2callback to prevent CSRF attacks.
    # This is omitted for simplicity in this MVP example.

    return RedirectResponse(authorization_url)

@app.get("/oauth2callback")
async def oauth2callback(request: Request):
    """
    Handles the redirect from Google after successful authorization.
    Exchanges the authorization code for access and refresh tokens, then stores them.
    """
    code = request.query_params.get("code")
    error = request.query_params.get("error")

    if error:
        print(f"OAuth error: {error}")
        return RedirectResponse(url=FRONTEND_URL + "/?auth_status=failed&error=" + error)

    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization code not found in callback."
        )

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

    try:
        flow.fetch_token(code=code)

        credentials = flow.credentials

        # Store tokens in the in-memory dictionary.
        # In a production application, these would be securely stored in a database
        # associated with the authenticated user's ID.
        user_tokens_store[TEST_USER_ID] = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
            "expiry": credentials.expiry.isoformat()
        }
        
        print(f"Tokens successfully saved for user {TEST_USER_ID}.")

        return RedirectResponse(url=FRONTEND_URL + "/?auth_status=success")

    except Exception as e:
        print(f"Error exchanging code for tokens: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to exchange authorization code: {e}"
        )