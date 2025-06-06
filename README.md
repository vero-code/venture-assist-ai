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

1️⃣ IdeaValidatorAgent		-> get_validator

2️⃣ PitchDeckGeneratorAgent	-> get_pitch

4️⃣ SummarySaverAgent		-> get_summary

5️⃣ LogoCreatorAgent		-> get_logo

6️⃣ MeetMakerAgent		    -> get_meeting