# backend/tools.py
from typing import Optional, List

# --- Tool Function Definitions ---
# Each function represents a core operation for its corresponding agent.

# Tool for IdeaValidatorAgent
def get_validator(idea: str, detailed_feedback: bool = False) -> dict:
    """
    Validates a startup idea and provides feedback on its potential and viability.
    Args:
        idea (str): Description of the startup idea.
        detailed_feedback (bool): If True, provide more detailed feedback.
    Returns:
        dict: Validation status and message.
    """
    print(f"--- Tool: get_validator called for idea: {idea} ---")
    if "crypto" in idea.lower() or "blockchain" in idea.lower():
        if detailed_feedback:
            return {"status": "needs_improvement", "feedback": "The provided 'crypto' idea is too broad. To properly validate it, I need more specifics. For example: what problem does your crypto idea solve? What is your target market? What is your business model? What is your competitive advantage? The crypto market is highly volatile and regulated across different jurisdictions. A more detailed description is required for proper validation. Currently, the idea is marked as needing improvement."}
        else:
            return {"status": "needs_improvement", "feedback": "The idea is too general, more details are required."}
    return {"status": "valid", "feedback": "The idea seems promising. You can proceed with market research."}

# Tool for MarketResearcherAgent
def get_research(topic: str) -> dict:
    """
    Conducts general market research on a given topic, including market size and key competitors.
    Args:
        topic (str): The topic or industry for research.
    Returns:
        dict: Market research results.
    """
    print(f"--- Tool: get_research called for topic: {topic} ---")
    # Placeholder for actual market research
    if "fintech" in topic.lower():
        return {"summary": "The fintech market is growing rapidly, with strong competition. The potential for innovation is high.", "market_size_usd_billion": 1500, "main_competitors": ["Leading Payment Processors", "Digital Banks", "Investment Platforms"]}
    return {"summary": f"General research on '{topic}' shows growth potential, but deeper analysis is needed.", "details": "No specific data available."}

# Tool for PitchDeckGeneratorAgent
def get_pitch(idea_summary: str, sections: Optional[List[str]] = None) -> str:
    """
    Generates a draft or sections of a pitch deck based on the provided idea.
    Args:
        idea_summary (str): A brief description of the startup idea.
        sections (List[str], optional): A list of specific sections to generate (e.g., "Problem", "Solution", "Market").
    Returns:
        str: The generated pitch deck text or its sections.
    """
    print(f"--- Tool: get_pitch called for idea: {idea_summary}, sections: {sections} ---")
    if not sections:
        sections = ["Problem", "Solution", "Market", "Team"]
    
    generated_content = []
    generated_content.append(f"**Pitch Deck for '{idea_summary}'**\n\n")
    
    for section in sections:
        if section.lower() == "problem":
            generated_content.append("## Problem\nThe existing problem is that users face [Describe user pain point].\n\n")
        elif section.lower() == "solution":
            generated_content.append("## Solution\nOur innovative solution offers [Describe your solution] to effectively address this problem.\n\n")
        elif section.lower() == "market":
            generated_content.append("## Market\nOur target market is [Market Size] and has [Growth Trends].\n\n")
        elif section.lower() == "team":
            generated_content.append("## Team\nOur team consists of [Experience and key members], ready to execute this vision.\n\n")
        else:
            generated_content.append(f"## {section}\n[Content for '{section}' section]\n\n")

    return "".join(generated_content)

# Tool for SummarySavingAgent
def get_summary(content_to_summarize: str, save_to_drive: bool = False) -> str:
    """
    Creates a brief summary of the provided content and can save it (e.g., as a PDF)
    and upload it to Google Drive.
    Args:
        content_to_summarize (str): Long text or report to be summarized.
        save_to_drive (bool): If True, generate a PDF and attempt to save it to Google Drive.
    Returns:
        str: The condensed summary and saving information.
    """
    print(f"--- Tool: get_summary called for content length: {len(content_to_summarize)} ---")
    # Simple placeholder for summarization
    summary = f"Brief summary: '{content_to_summarize[:150]}...' The final report is ready."
    
    if save_to_drive:
        # Simulate PDF generation and saving
        file_name = f"Startup_Report_Summary_{hash(content_to_summarize)}.pdf"
        drive_link = f"https://mock-drive.google.com/link/{file_name}"
        return f"{summary} A PDF report has been generated and saved to Google Drive: {drive_link}"
    
    return summary

# Tool for LogoCreatorAgent
def get_logo(idea_description: str) -> str:
    """
    Generates a concept and URL for a logo based on the startup idea description.
    Args:
        idea_description (str): Description of the startup idea for logo creation.
    Returns:
        str: URL of the generated logo and its brief description.
    """
    print(f"--- Tool: get_logo called for idea: {idea_description} ---")
    # Placeholder for logo generation
    logo_concept = f"A minimalistic logo inspired by '{idea_description}', using modern fonts and geometric shapes."
    logo_url = f"https://picsum.photos/seed/{hash(idea_description)}/200/200" # Simple URL placeholder
    return f"Logo concept generated: '{logo_concept}'. Preview: {logo_url}"

# Tool for MeetMakerAgent
def get_meeting(purpose: str, participant_email: str, preferred_date: str = "") -> str:
    """
    Organizes a meeting (e.g., with an investor) for the specified purpose and participant.
    May suggest available slots.
    Args:
        purpose (str): The purpose of the meeting (e.g., "Investor meeting", "Project discussion").
        participant_email (str): The email of the participant with whom to organize the meeting.
        preferred_date (str, optional): Preferred date for the meeting (e.g., "tomorrow", "next week").
    Returns:
        str: Confirmation of meeting organization or a request for clarification.
    """
    print(f"--- Tool: get_meeting called for purpose: {purpose}, participant: {participant_email} ---")
    # Placeholder for meeting scheduling
    if "@" in participant_email:
        return f"Attempting to organize a meeting '{purpose}' with {participant_email}. Please await email confirmation. Preferred date: {preferred_date if preferred_date else 'any available'}."
    return "Failed to organize meeting. Please ensure the purpose and a valid participant email are provided."