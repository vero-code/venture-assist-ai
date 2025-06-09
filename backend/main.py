# backend/main.py
import os
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from .agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.genai.types import Content, Part
from .state import user_tokens_store, TEST_USER_ID

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
FRONTEND_URL = os.getenv("FRONTEND_URL")

if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, GOOGLE_PROJECT_ID]):
    raise ValueError("Google API credentials are not set in environment variables. Please check your .env file.")

if not FRONTEND_URL:
    raise ValueError("FRONTEND_URL is not set in environment variables. Please check your .env file.")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

APP_NAME = "venture_assist_ai"
SESSION_ID = "default_session"

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)

@app.on_event("startup")
async def startup_event():
    try:
        await session_service.get_session(APP_NAME, TEST_USER_ID, SESSION_ID)
    except Exception:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=TEST_USER_ID,
            session_id=SESSION_ID
        )

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar"
]

# Pydantic model for incoming chat requests
class ChatRequest(BaseModel):
    query: str

@app.get("/")
async def read_root():
    return {"message": "Venture Assist AI Backend is running!"}

@app.post("/chat")
async def chat_with_ai(request: ChatRequest):
    """
    Processes user queries and returns AI responses.
    """
    try:
        run_config = RunConfig(streaming_mode=StreamingMode.NONE, max_llm_calls=100)
        content = Content(role="user", parts=[Part(text=request.query)])

        async for event in runner.run_async(
            user_id=TEST_USER_ID,
            session_id=SESSION_ID,
            new_message=content,
            run_config=run_config
        ):
            if event.is_final_response():
                return {"response": event.content.parts[0].text}

        raise HTTPException(status_code=500, detail="No final response from agent.")
    
    except Exception as e:
        print(f"❌ Error in root agent: {e}")
        raise HTTPException(status_code=500, detail="Agent failed to process your query.")

@app.get("/auth/google")
async def google_auth():
    """
    Initiates Google's OAuth flow.
    Redirects the user to Google's consent page.
    """
    from google_auth_oauthlib.flow import Flow

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
        access_type='offline',
        include_granted_scopes='true'
    )

    return RedirectResponse(authorization_url)

@app.get("/oauth2callback")
async def oauth2callback(request: Request):
    """
    Handles the redirect from Google after successful authorization.
    Exchanges the authorization code for access and refresh tokens, then stores them.
    """
    from google_auth_oauthlib.flow import Flow

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

        user_tokens_store[TEST_USER_ID] = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
            "expiry": credentials.expiry.isoformat()
        }

        return RedirectResponse(url=FRONTEND_URL + "/?auth_status=success")

    except Exception as e:
        print(f"Error exchanging code for tokens: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to exchange authorization code: {e}"
        )