# backend/agent.py
from google.adk.agents import Agent
from agents import ALL_SUB_AGENTS
from config import MODEL_GEMINI_PRO
import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- Congiguration ---
load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key GOOGLE_API_KEY not found. Please check your .env file.")

genai.configure(api_key=api_key)

# --- Main Coordinator Agent (root_agent) ---
root_agent = Agent(
    name="VentureCoordinatorAgent",
    model=MODEL_GEMINI_PRO,
    instruction="You are a versatile assistant for startups and venture capital. Your main task is to understand user requests related to startup ideas, their development, and promotion, and effectively delegate these tasks to the most suitable specialized agent on your team. "
                "If the user wants to evaluate or validate an idea, delegate to the 'IdeaValidatorAgent'. "
                "For requests related to market or competitor research, use the 'MarketResearcherAgent'. "
                "If the user wants to create or improve a pitch deck, refer to the 'PitchDeckGeneratorAgent'. "
                "To summarize information and save reports, delegate to the 'SummarySaverAgent'. "
                "For logo creation requests, use the 'LogoCreatorAgent'. "
                "And for scheduling meetings, for example with investors, direct requests to the 'MeetMakerAgent'. "
                "Be polite, professional, and clear in your responses. If you cannot process a request, politely inform the user.",
    description="The main coordinator of all Venture Assist AI operations, delegating requests to specialized agents.",
    tools=[],
    sub_agents=ALL_SUB_AGENTS,
)