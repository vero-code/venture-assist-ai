# backend/tools.py
from typing import Optional, List
import google.generativeai as genai
import json
from google.adk.tools.tool_context import ToolContext
from datetime import datetime, timezone
from .config import (
    MODEL_GEMINI_FLASH,
    MODEL_GEMINI_PRO
)
import requests
from .state import user_tokens_store, TEST_USER_ID
import traceback

GOOGLE_CALENDAR_API_ENDPOINT = 'https://www.googleapis.com/calendar/v3/calendars/primary/events';

# --- Tool Function Definitions ---
# Each function represents a core operation for its corresponding agent.

# Tool for IdeaValidatorAgent
def get_validator(idea: str, detailed_feedback: bool = False) -> dict:
    """
    Validates a startup idea and provides feedback on its potential and viability.
    Uses an LLM for deeper analysis.
    Args:
        idea (str): Description of the startup idea.
        detailed_feedback (bool): If True, provide more detailed feedback.
    Returns:
        dict: Validation status and message.
    """
    print(f"--- Tool: get_validator called for idea: {idea} ---")

    # Prompt for the LLM to act as a validator
    system_prompt = f"""
    You are an expert in startup idea validation. Your task is to analyze the provided startup idea and assess its potential and viability.
    Evaluate the idea based on the following criteria:
    1.  **Novelty/Innovativeness**: How unique or innovative is the idea?
    2.  **Problem Solved**: What problem does it solve, and how relevant is it?
    3.  **Target Audience**: Who is the target audience, and how large/accessible is it?
    4.  **Competitive Advantage**: What differentiates this idea from existing solutions or potential competitors?
    5.  **Scalability**: How easily can the idea be expanded?
    6.  **Potential Risks**: What are the main risks associated with implementing this idea (market, technical, financial)?

    Your response must be in JSON format, containing:
    - `status` (str): 'valid', 'needs_improvement', 'risky', 'novel' (you can add your own statuses)
    - `short_feedback` (str): A brief conclusion (1-2 sentences).
    - `detailed_feedback` (str, optional): A detailed analysis based on the criteria, if `detailed_feedback` is True.

    Example JSON response:
    ```json
    {{
        "status": "valid",
        "short_feedback": "The mobile app idea for finding nannies has high potential but requires competitor research.",
        "detailed_feedback": "Novelty: Analogues exist, but UI/UX can be improved. Problem: Relevant for busy parents. Target Audience: Parents with children, fairly large. Competitive Advantage: A unique selling proposition needs to be developed. Scalability: High. Risks: High competition, trust and safety issues."
    }}
    ```
    """

    user_message = f"Evaluate the following startup idea: {idea}"

    try:
        # Create a model for validation
        model = genai.GenerativeModel(
            MODEL_GEMINI_PRO,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        # Send request to LLM
        response = model.generate_content(
            [system_prompt, user_message]
        )

        # Parse JSON response
        validation_result = json.loads(response.text)

        if detailed_feedback:
            return {
                "status": validation_result.get("status", "unknown"),
                "feedback": validation_result.get("detailed_feedback", validation_result.get("short_feedback", "No specific feedback provided."))
            }
        else:
            return {
                "status": validation_result.get("status", "unknown"),
                "feedback": validation_result.get("short_feedback", "No specific feedback provided.")
            }

    except Exception as e:
        print(f"Error during LLM validation: {e}")
        return {"status": "error", "feedback": f"Failed to perform detailed validation due to an internal error: {str(e)}."}

# Tool for MarketResearcherAgent
def get_research(topic: str) -> dict:
    """
    Conducts general market research on a given topic, including market size,
    key competitors, current trends, and future outlook using an LLM.
    Args:
        topic (str): The topic or industry for research.
    Returns:
        dict: Market research results.
    """
    print(f"--- Tool: get_research called for topic: {topic} ---")

    try:
        model = genai.GenerativeModel(MODEL_GEMINI_PRO)

        prompt = (
            f"Conduct detailed market research on the '{topic}' industry. "
            "Provide information on the following aspects in a structured format:\n"
            "1. **Market Size:** Estimate the current market size (e.g., in USD billion/trillion).\n"
            "2. **Key Competitors:** List 3-5 major players.\n"
            "3. **Current Trends:** Describe 2-3 significant trends.\n"
            "4. **Future Outlook:** Provide a brief outlook (e.g., growth potential, challenges).\n"
            "5. **Innovation Potential:** Briefly comment on areas for innovation.\n\n"
            "Format the response as a clear, concise summary suitable for a business report. "
            "Do not include any introductory or concluding phrases like 'Here is the research...'. "
            "Just provide the structured information."
        )

        print(f"--- Tool: Calling LLM for research on '{topic}' with model: {MODEL_GEMINI_PRO} ---")
        response = model.generate_content(prompt)

        research_summary = response.text
        print(f"--- Tool: LLM generated research summary. ---")

        return {
            "status": "success",
            "summary": research_summary,
            "topic": topic
        }

    except Exception as e:
        print(f"--- Tool ERROR: Failed to conduct research for '{topic}'. Error: {e} ---")
        return {
            "status": "error",
            "error_message": f"Failed to conduct research for '{topic}' due to an internal error: {e}"
        }

# Tool for PitchDeckGeneratorAgent
def get_pitch(idea_summary: str, sections: Optional[List[str]] = None) -> str:
    """
    Generates a draft or sections of a pitch deck based on the provided idea summary,
    using an LLM to generate compelling content for each specified section.
    Args:
        idea_summary (str): A brief description of the startup idea.
        sections (List[str], optional): A list of specific sections to generate
                                        (e.g., "Problem", "Solution", "Market", "Team", "Business Model", "Competition", "Financials", "Call to Action").
                                        Defaults to ["Problem", "Solution", "Market", "Team"] if not provided.
    Returns:
        str: The generated pitch deck text or its sections.
    """
    print(f"--- Tool: get_pitch called for idea: {idea_summary}, sections: {sections} ---")

    if not sections:
        sections = ["Problem", "Solution", "Market", "Team"]

    generated_content = []
    generated_content.append(f"# Pitch Deck for '{idea_summary}'\n\n")

    try:
        model = genai.GenerativeModel(MODEL_GEMINI_FLASH)

        for section in sections:
            section_title = section.capitalize()
            prompt = (
                f"Generate a concise and compelling paragraph for the '{section_title}' section "
                f"of a startup pitch deck. The startup idea is: '{idea_summary}'.\n\n"
                f"Focus on key information relevant to a pitch. Do not include any introductory or "
                f"concluding phrases outside of the generated section content. Start directly with the content for the section. "
                f"Make sure the content is professional and persuasive."
            )

            if section.lower() == "problem":
                prompt += " Specifically, describe the core pain point or unmet need that the idea addresses."
            elif section.lower() == "solution":
                prompt += " Specifically, describe how the idea innovatively solves the identified problem."
            elif section.lower() == "market":
                prompt += " Specifically, describe the target market, its size, and growth potential."
            elif section.lower() == "team":
                prompt += " Specifically, describe the key team members and their relevant experience or unique advantages."

            print(f"--- Tool: Calling LLM for '{section_title}' section with model: {MODEL_GEMINI_FLASH} ---")
            response = model.generate_content(prompt)
            section_content = response.text
            print(f"--- Tool: LLM generated content for '{section_title}'. ---")

            generated_content.append(f"## {section_title}\n")
            generated_content.append(section_content)
            generated_content.append("\n\n")

    except Exception as e:
        print(f"--- Tool ERROR: Failed to generate pitch deck content for '{idea_summary}'. Error: {e} ---")
        return f"Error generating pitch deck: {e}"

    return "".join(generated_content)

# Tools for SummarySavingAgent
def get_summary(content_to_summarize: str, tool_context: ToolContext) -> str:
    """
    Creates a brief, high-quality summary of the provided content using an LLM.
    and stores it in the session state for later saving.
    Args:
        content_to_summarize (str): Long text or report to be summarized.
        tool_context (ToolContext): ADK ToolContext for accessing session state.
    Returns:
        str: The condensed summary.
    """
    print(f"--- Tool: get_summary called for content length: {len(content_to_summarize)} ---")

    MIN_CONTENT_LENGTH = 50 # Minimum number of characters for summarization
    if len(content_to_summarize) < MIN_CONTENT_LENGTH:
        return f"Summary: The provided content is too short (less than {MIN_CONTENT_LENGTH} characters) to generate a meaningful summary. Content received: '{content_to_summarize}'"

    try:
        model = genai.GenerativeModel(MODEL_GEMINI_FLASH)

        prompt = (
            f"Please provide a concise, factual, and neutral summary of the following content. "
            "Focus on the main points and key information. "
            "The summary should be no longer than 3-5 sentences unless the content is extremely long, "
            "in which case provide a slightly longer but still concise summary. "
            "Do not include any introductory phrases like 'Here is a summary...' or 'This content is about...'. "
            "Just provide the summary directly.\n\n"
            "Content to summarize:\n"
            f"{content_to_summarize}"
        )

        print(f"--- Tool: Calling LLM for summarization with model: {MODEL_GEMINI_FLASH} ---")
        response = model.generate_content(prompt)
        llm_summary = response.text
        print(f"--- Tool: LLM generated summary. ---")

        # Save summary to session state
        tool_context.state["last_summary"] = llm_summary
        tool_context.state["last_summary_timestamp"] = datetime.datetime.now()
        print(f"--- Tool: Summary saved to session state via tool_context. Current state: {tool_context.state} ---")

        return f"Summary: {llm_summary}"

    except Exception as e:
        print(f"--- Tool ERROR: Failed to generate summary. Error: {e} ---")
        return f"Error: Could not generate a summary due to an internal LLM error: {e}"

def get_saver(content_to_save: Optional[str] = None, file_name: Optional[str] = None, tool_context: ToolContext = None) -> str:
    """
    Saves content to Google Drive using provided credentials.
    Prioritizes content from session state if available and no explicit content_to_save is provided.
    """
    from .main import user_tokens_store, TEST_USER_ID

    print(f"--- Tool: get_saver called. Content provided directly: {content_to_save is not None}, file_name: {file_name} ---")

    actual_content_to_save = content_to_save

    if tool_context is None:
        return "Error: ToolContext not provided. Cannot access session state for saving."
    
    # if content_to_save is not provided, try to take it from the state via tool_context
    if actual_content_to_save is None:
        if tool_context.state.get("last_summary"):
            actual_content_to_save = tool_context.state["last_summary"]
            print(f"--- Tool: Using last_summary from session state (tool_context) for saving. ---")
        else:
            # If there is no direct content or summary in memory
            return "Failed to save. No substantial content provided or found in session memory for saving. Please provide text or generate a summary first."
    
    if not actual_content_to_save or len(actual_content_to_save) < 10:
        return "Failed to save. The content for saving is too short or empty."

    if not file_name:
        safe_content_part = "".join(c for c in actual_content_to_save[:30] if c.isalnum() or c.isspace()).strip().replace(" ", "_")
        if not safe_content_part: # Fallback if first part is non-alphanumeric
            safe_content_part = "document"
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{safe_content_part}_{timestamp}.txt"

        if len(file_name) > 100:
            file_name = file_name[:90] + ".txt"
        print(f"--- Tool: Generated file_name: {file_name} ---")

    tokens = user_tokens_store.get(TEST_USER_ID)
    if not tokens or "token" not in tokens:
        return "Error: No valid Google access token. Please authorize via /auth/google."

    access_token = tokens["token"]

    metadata = {
        'name': file_name,
        'mimeType': 'text/plain'
    }

    files = {
        'metadata': ('metadata', json.dumps(metadata), 'application/json'),
        'file': (file_name, actual_content_to_save, 'text/plain')
    }

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    try:
        upload_url = 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart'
        response = requests.post(upload_url, headers=headers, files=files)
        response.raise_for_status()
        file_id = response.json().get('id')

        tool_context.state["last_summary"] = None
        tool_context.state["last_summary_timestamp"] = None
        print(f"--- Tool: Cleared session state after saving. ---")

        if file_id:
            return f"✅ Saved to Google Drive: https://drive.google.com/file/d/{file_id}/view"
        else:
            return "⚠️ Upload succeeded but file ID was not returned."

    except Exception as e:
        print(f"❌ Upload error: {e}")
        return f"❌ Failed to upload to Google Drive: {e}"

# Tool for LogoCreatorAgent
def get_logo(idea_description: str) -> str:
    """
    Generates a creative concept and a placeholder URL for a logo based on the startup idea description,
    using an LLM to craft the concept.
    Args:
        idea_description (str): Description of the startup idea for logo creation.
    Returns:
        str: Description of the generated logo concept and its preview URL.
    """
    print(f"--- Tool: get_logo called for idea: {idea_description} ---")

    try:
        model = genai.GenerativeModel(MODEL_GEMINI_PRO)

        prompt = (
            f"Generate a concise and creative concept for a startup logo based on the following idea description:\n"
            f"'{idea_description}'\n\n"
            "The concept should include:\n"
            "1. **Main elements/icons:** What visual elements or symbols should be present?\n"
            "2. **Color palette:** Suggest 2-3 primary colors and their mood/meaning.\n"
            "3. **Typography style:** Suggest a font style (e.g., modern sans-serif, classic serif, bold, playful).\n"
            "4. **Overall mood/feeling:** What emotion or impression should the logo convey?\n"
            "Keep it brief, 3-5 sentences total, focusing on key design aspects. Do not include any introductory or concluding phrases. "
            "Just provide the logo concept directly."
        )

        print(f"--- Tool: Calling LLM for logo concept with model: {MODEL_GEMINI_PRO} ---")
        response = model.generate_content(prompt)
        llm_logo_concept = response.text
        print(f"--- Tool: LLM generated logo concept. ---")

        logo_url = f"https://picsum.photos/seed/{hash(idea_description)}/200/200"
        
        return f"Logo concept generated:\n\n'{llm_logo_concept}'.\n\nPreview (placeholder): {logo_url}"

    except Exception as e:
        print(f"--- Tool ERROR: Failed to generate logo concept for '{idea_description}'. Error: {e} ---")
        return f"Error generating logo concept: {e}"

# Tool for MeetMakerAgent
def extract_meeting_slots(preferred_date: str, model_name: str = MODEL_GEMINI_FLASH) -> list:
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    prompt = (
        f"You are an assistant helping to schedule meetings. The current date and time is: {now_utc}.\n"
        f"The user wants to schedule a meeting on '{preferred_date}'.\n"
        "Generate 2–3 time slots in the future, in UTC timezone, each exactly 1 hour long.\n"
        "Use ISO 8601 format, and make sure all slots are after the current time.\n"
        "Example:\n"
        "- 2025-06-15T10:00:00Z to 2025-06-15T11:00:00Z\n"
        "- 2025-06-16T14:00:00Z to 2025-06-16T15:00:00Z\n"
        "Only return the list. No explanation."
    )

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        slots = [line.strip("- ").strip() for line in response.text.splitlines() if line.startswith("-")]
        print(f"--- Tool: Extracted slots: {slots} ---")
        return slots
    except Exception as e:
        print(f"❌ Error extracting time slots: {e}")
        return []

def get_meeting(purpose: str, participant_email: str, preferred_date: str) -> str:
    """
    Schedules a real meeting in Google Calendar with Google Meet link.
    """
    print(f"--- Tool: get_meeting called for purpose: {purpose}, participant: {participant_email}, preferred_date: '{preferred_date}' ---")

    if "@" not in participant_email or "." not in participant_email:
        print(f"--- Tool: Invalid email format for participant: {participant_email} ---")
        return "Failed to organize meeting. Please ensure a valid participant email is provided (e.g., 'name@example.com')."

    slots = extract_meeting_slots(preferred_date)
    print(f"--- Tool: Extracted slots: {slots} ---")
    if not slots:
        return "❌ Failed to interpret the preferred date. Please try a more specific one."
    
    try:
        first_slot = slots[0]
        start_str, end_str = [s.strip() for s in first_slot.split("to")]
        start_dt = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end_str.replace("Z", "+00:00"))
        print(f"--- Tool: Parsed times: {start_dt} to {end_dt} ---")
    except Exception as e:
        return f"❌ Failed to parse generated time slot: {e}"
    
    tokens = user_tokens_store.get(TEST_USER_ID)
    if not tokens or "token" not in tokens:
        return "❌ No valid Google access token. Please authorize via /auth/google."
    
    access_token = tokens["token"]

    event_data = {
        "summary": purpose,
        "description": f"Meeting with {participant_email}",
        "start": {"dateTime": start_dt.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": "UTC"},
        "attendees": [{"email": participant_email}],
        "conferenceData": {
            "createRequest": {
                "requestId": f"meet-{datetime.utcnow().timestamp()}",
                "conferenceSolutionKey": {"type": "hangoutsMeet"}
            }
        },
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    params = {"conferenceDataVersion": 1}
    
    try:
        response = requests.post(
            GOOGLE_CALENDAR_API_ENDPOINT,
            headers=headers,
            params=params,
            data=json.dumps(event_data)
        )

        print(f"--- Tool: Calendar API response code: {response.status_code} ---")
        print(f"--- Tool: Calendar API raw response: {response.text} ---")

        response.raise_for_status()
        event = response.json()

        meet_link = event.get("hangoutLink")
        if not meet_link and "conferenceData" in event:
            entry_points = event["conferenceData"].get("entryPoints", [])
            for entry in entry_points:
                if entry.get("entryPointType") == "video":
                    meet_link = entry.get("uri")
                    break

        print("--- Tool: Full event created ---")
        print(json.dumps(event, indent=2))
        return f"✅ Meeting scheduled on {start_dt} with {participant_email}. Google Meet link: {meet_link or '[None]'}"

    except Exception as e:
        traceback.print_exc()
        print(f"--- Tool ERROR: Failed to generate meeting confirmation for '{participant_email}'. Error: {e} ---")
        return f"An error occurred while trying to organize the meeting: {e}. Please try again later."