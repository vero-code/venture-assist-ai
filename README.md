# Venture Assist AI

Smart AI assistant for startups. From idea to public presentation – multi-agent system on Google Cloud ADK (Agent Development Kit) leads you to success. The project is inspired by the tasks of the hackathon ["AI Agent Development Kit Hackathon with Google Cloud"](https://googlecloudmultiagents.devpost.com/).


## Architecture

At the top level, the **Coordinator/Dispatcher pattern** is used for the `venture_coordinator_agent`, which redirects the user to the appropriate specialized agents. The complete architecture will be shown in the final diagram.


## Technologies

- ADK ([Agent Development Kit](https://google.github.io/adk-docs/)), thanks [API documentation](https://google.github.io/adk-docs/api-reference/python/index.html)
- Google Cloud SDK
- Python v3.13.4, Uvicorn
- Node.js v22.16.0
- JavaScript, React, Vite
- Tailwindcss


### 🗨️ Google Cloud Services

- Google AI Studio
- Google AOuth
- Google Calendar
- Google Meet
- Google Slides


## 📁 Structure

```
venture-assist-ai/
│
├── backend/
│   ├── __init__.py        # Initialize the package
│   ├── agent.py           # Agent coordinator
│   ├── agents.py          # Subagents
│   ├── config.py          # Constants of models
│   ├── main.py            # Entry point
│   ├── requirements.txt   # Dependencies
│   ├── state.py           # To store state
│   └── tools.py           # Definitions of instruments
│
├── frontend/              # Style & Ui design
│   └── ...
│
├── multi_tool_agent/      # Example a simple agent
│   └── ...
│
└── .env.example           # Environment variables
```

> A simple agent was developed using the [Quickstart](https://google.github.io/adk-docs/get-started/quickstart/) documentation.


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

4️⃣ **SummarySaverAgent**

 -> `get_summary`
 
 - **Capabilities:** Summarizes provided lengthy text.

- **User Benefit:** Delivers a concise summary of notes on paper of a budding startup.

- **Improvement:** Avoids unnecessary LLM calls for trivial cases using length check.

-> `get_saver`

- **Capabilities:** Gets summary from memory and saves in Google Drive.

- **User Benefit:** Shows info message if memory is empty.

5️⃣ **LogoCreatorAgent** -> `get_logo`
   - **Capabilities:** Generates a logo concept for a startup idea.
   - **User Benefit:** Suggests a creative logo idea with design and style descriptions.
   - **Improvement:** Saves the logo description in Google Slides for future image creation.

6️⃣ **MeetMakerAgent** -> `get_meeting`
   - **Capabilities:** Organizes a meeting with a specified participant.
   - **User Benefit:** Extracts a date from the user input and writes the meeting to the calendar.


### 💾 Agent Memory

The memory of the `SummarySaverAgent` is implemented via `ToolContext`, which provides an interface for interacting with the session state (`tool_context.state`). `SessionService` physically ensures the persistence of this state.

Thus, after summarization, the `last_summary` is stored in `tool_context.state`, and upon a subsequent save request, the agent utilizes this information either directly from arguments passed by the LLM or by accessing `tool_context.state["last_summary"]`.


### 🔒 Authorization moment

Implemented Google's basic authorization mechanism using two endpoints:

- `/auth/google` initiates the Google authorization process and redirects the user to the consent page.

- `/oauth2callback` accepts the authorization code from Google, exchanges it for access and refresh tokens, and then stores them.


### 🎥 Meet Planning

`MeetMakerAgent` uses the `get_meeting` tool, which calls `extract_meeting_slots` — a function powered by an LLM to propose meeting times.

Then Google services come into play:

- `Google Calendar` is used to create the event.

- `Google Meet` is enabled automatically via the Calendar API when ads conference Data.


### 📒 Slide creation

The `LogoCreatorAgent` uses the `get_logo` tool to use the `Gemini` model to generate a logo concept (including icon, colors, font, and mood). Then, interaction occurs with the Google Slides API: creates a new presentation, adds a blank slide to it, and inserts the generated logo concept into a text field on this slide. At the end, the function returns a confirmation of creation and a link to the created slide.


## 🔬 Testing

### IdeaValidatorAgent

-> get_validator

Query:
```
Test the idea: a mobile app for finding nannies.
```

Query:
```
What do you think about the idea of ​​the smart waste diversion system for households startup?
```


### MarketResearcherAgent

-> get_research

Query: 
```
Conduct market research on the renewable energy sector.
```

Query: 
```
Research the current state of the AI in healthcare market.
```


### PitchDeckGeneratorAgent

-> get_pitch

Query: 
```
Generate a pitch deck for a web app that helps finding houses with AI.
```

Query: 
```
Create a pitch deck for a AI-powered personalized learning platform, include sections for Problem, Solution, and Team.
```


### SummarySaverAgent

-> get_summary

Query: 

```
Summarize idea: An idea came to me, it seems a bit crazy, but the more I think about it, the more I like it. What if we make a smart mirror that helps track your mental state? Like, in the morning and in the evening you just go to the mirror, and it, looking at your facial expression, listening to your voice, intonation, evaluating your reactions, notices if you are burnt out, depressed or just tired. And it can gently suggest: "do a breathing practice", "try to rest a little", or even "it's time to talk to someone". Everything is local or encrypted. It's like a caring AI assistant, but not intrusive.
```

-> get_saver

Query: 

```
Can you save it?
```

-> get_summary + get_saver

Query: 

```
Create summary and save: Listen, I have a cool idea. Why not make personalized tea based on DNA? Like, a person takes a simple test (like for genetics - saliva), plus fills out a questionnaire: how he sleeps, what he does, what flavors he likes. And then AI or an algorithm selects a tea blend for him - with the right herbs, vitamins, flavors and even the effect (calming, energy, recovery, etc.). You can do it as a subscription: every month a person gets "his" tea. It's like genetics + healthy lifestyle + a bit of a geek.
```


### LogoCreatorAgent

-> get_logo

Query:

```
Generate a logo concept for a startup that builds eco-friendly packaging solutions.
```

Query:
```
Create a logo for a fitness app for seniors.
```


### MeetMakerAgent

-> get_meeting

Query: 

```
Arrange a meeting with investor@gmail.com next week to discuss the startup.
```

Query: 
```
Schedule a project discussion with alice@company.com for June 15th.
```

Query:
```
Organize an investor meeting with bob@example.com for tomorrow.
```


## 📄 License & contribution

This project is licensed under the MIT License. When using this software, please remember to provide appropriate attribution to the original author.