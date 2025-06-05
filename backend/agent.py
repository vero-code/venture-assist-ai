# backend/src/agent.py
from google.adk.agents import Agent

def get_validator(idea: str) -> dict:
    """
    Validates a startup idea based on predefined simple criteria.
    Args:
        idea (str): The startup idea to validate.
    Returns:
        dict: A dictionary containing validation status and feedback.
    """
    idea_lower = idea.lower()
    feedback = []
    is_valid = True

    if "selling homes with built-in ai" in idea_lower:
        feedback.append("This idea is relevant to the example. Good start!")
    elif "selling homes" in idea_lower:
        feedback.append("The idea of 'selling homes' is common. Consider adding a unique differentiator.")
    elif "ai" in idea_lower:
        feedback.append("Integrating AI is a strong point. Elaborate on the specific AI application.")
    else:
        feedback.append("The idea lacks specificity. Please provide more details to validate.")
        is_valid = False

    if "crypto" in idea_lower or "blockchain" in idea_lower:
        feedback.append("Note: The crypto/blockchain market can be volatile. Consider regulatory aspects.")

    if len(idea) < 20:
        feedback.append("The idea description is too short. Please provide more context.")
        is_valid = False

    return {
        "status": "success" if is_valid else "warning",
        "validation_status": "Valid" if is_valid else "Needs Improvement",
        "feedback": feedback,
        "original_idea": idea
    }

root_agent = Agent(
    name="idea_validator_agent",
    model="gemini-1.5-flash",
    description="Agent for validating startup ideas based on predefined criteria.",
    instruction=(
        "You are an expert startup idea validator. Your primary role is to "
        "**evaluate user-provided startup ideas against a set of predefined criteria** "
        "and provide feedback based on this assessment. Focus on the core validation."
    ),
    tools=[get_validator],
)