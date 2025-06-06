# backend/agents.py
from google.adk.agents import Agent
from .tools import (
    get_validator,
    get_research,
    get_pitch,
    get_summary,
    get_logo,
    get_meeting
)
from .config import (
    MODEL_GEMINI_FLASH,
    MODEL_GEMINI_PRO
)

# --- Specialized Agent Definitions ---
idea_validator_agent = None
try:
    idea_validator_agent = Agent(
        name="IdeaValidatorAgent",
        model=MODEL_GEMINI_FLASH,
        instruction="You are an expert in startup idea validation. Your task is to thoroughly analyze provided ideas and give constructive feedback, pointing out potential problems and areas for improvement. Use only the 'get_validator' tool to check ideas.",
        description="An agent specializing in validating new startup ideas and providing feedback.",
        tools=[get_validator]
    )
    print(f"✅ Sub-Agent '{idea_validator_agent.name}' redefined.")
except Exception as e:
    print(f"❌ Error redefining IdeaValidatorAgent: {e}")

market_researcher_agent = None
try:
    market_researcher_agent = Agent(
        name="MarketResearcherAgent",
        model=MODEL_GEMINI_PRO,
        instruction="You are an expert in market research and competitor analysis. Use only the 'get_research' tool to gather and analyze information. Answer questions about market size, trends, and competitors.",
        description="An agent for conducting general market research and competitor analysis.",
        tools=[get_research]
    )
    print(f"✅ Sub-Agent '{market_researcher_agent.name}' redefined.")
except Exception as e:
    print(f"❌ Error redefining MarketResearcherAgent: {e}")

pitch_deck_generator_agent = None
try:
    pitch_deck_generator_agent = Agent(
        name="PitchDeckGeneratorAgent",
        model=MODEL_GEMINI_FLASH,
        instruction="You are an expert in creating compelling pitch decks. Use only the 'get_pitch' tool to write pitch deck content. Your task is to help the user create a draft of a complete pitch deck.",
        description="An agent for generating pitch deck drafts and sections.",
        tools=[get_pitch]
    )
    print(f"✅ Sub-Agent '{pitch_deck_generator_agent.name}' redefined.")
except Exception as e:
    print(f"❌ Error redefining PitchDeckGeneratorAgent: {e}")

summary_saver_agent = None
try:
    summary_saver_agent = Agent(
        name="SummarySaverAgent",
        model=MODEL_GEMINI_FLASH,
        instruction="You are an agent responsible for collecting all necessary summaries, summarizing them, and saving them. Use only the 'get_summary' tool to process content.",
        description="An agent for summarizing content.",
        tools=[get_summary]
    )
    print(f"✅ Sub-Agent '{summary_saver_agent.name}' redefined.")
except Exception as e:
    print(f"❌ Error redefining SummarySaverAgent: {e}")

logo_creator_agent = None
try:
    logo_creator_agent = Agent(
        name="LogoCreatorAgent",
        model=MODEL_GEMINI_PRO,
        instruction="You are a creative agent specializing in logo concept creation. Use only the 'get_logo' tool to generate logo ideas and images. Respond by providing the logo concept and its URL.",
        description="An agent for creating project logos.",
        tools=[get_logo]
    )
    print(f"✅ Sub-Agent '{logo_creator_agent.name}' redefined.")
except Exception as e:
    print(f"❌ Error redefining LogoCreatorAgent: {e}")

meet_maker_agent = None
try:
    meet_maker_agent = Agent(
        name="MeetMakerAgent",
        model=MODEL_GEMINI_PRO,
        instruction="You are an assistant agent for meeting scheduling. Use only the 'get_meeting' tool to organize meetings with participants. Help users schedule meetings with investors or their team.",
        description="An agent for scheduling meetings with investors.",
        tools=[get_meeting]
    )
    print(f"✅ Sub-Agent '{meet_maker_agent.name}' redefined.")
except Exception as e:
    print(f"❌ Error redefining MeetMakerAgent: {e}")

# List of all subagents for easy import
ALL_SUB_AGENTS = [
    idea_validator_agent,
    market_researcher_agent,
    pitch_deck_generator_agent,
    summary_saver_agent,
    logo_creator_agent,
    meet_maker_agent
]