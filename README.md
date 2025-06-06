# Venture Assist AI

Smart AI assistant for startups. From idea to public presentation – multi-agent system on Google Cloud ADK (Agent Development Kit) leads you to success. The project is inspired by the tasks of the hackathon ["AI Agent Development Kit Hackathon with Google Cloud"](https://googlecloudmultiagents.devpost.com/).

## Architecture

At the top level, the **Coordinator/Dispatcher pattern** is used for the `venture_coordinator_agent`, which redirects the user to the appropriate specialized agents. The complete architecture will be shown in the final diagram.


## 📁 Structure

```
venture-assist-ai/
├── backend/
│   ├── __init__.py          # Initialize the package
│   ├── .env.example         # Environment variables
│   ├── agent.py             # Agent coordinator
│   ├── agents.py            # Subagents
│   ├── config.py            # Constants of models
│   ├── requirements.txt     # Dependencies
│   └── tools.py             # Definitions of instruments
└── frontend/
│   └── ...
└── multi_tool_agent/        # Example a simple agent
```

## ✨ Features

Total 7 agents (1 coordinator & 6 subagents):

1️⃣ **IdeaValidatorAgent** -> `get_validator`
   - **Capabilities:** Evaluates provided startup ideas.
   - **User Benefit:** Provides intelligent analysis and detailed feedback on the idea.

2️⃣ **MarketResearcherAgent** -> `get_research`
   - **Capabilities:** Conducts market research on a given topic.
   - **User Benefit:** Generates a detailed report on market size, competitors, and trends.

3️⃣ **PitchDeckGeneratorAgent** -> `get_pitch`
   - **Capabilities:** Creates a draft pitch deck for a startup.
   - **User Benefit:** Forms compelling content for key presentation sections.

4️⃣ **SummarySaverAgent** -> `get_summary`
   - **Capabilities:** Summarizes provided lengthy text.
   - **User Benefit:** Delivers a concise and informative summary of large documents.

5️⃣ **LogoCreatorAgent** -> `get_logo`
   - **Capabilities:** Generates a logo concept for a startup idea.
   - **User Benefit:** Suggests a creative logo idea with design and style descriptions.

6️⃣ **MeetMakerAgent** -> `get_meeting`
   - **Capabilities:** Organizes a meeting with a specified participant.
   - **User Benefit:** Confirms meeting details and suggests next steps for scheduling.