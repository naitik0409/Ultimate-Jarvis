# JARVIS — Voice AI Assistant + Coding Agent

A terminal-based voice AI assistant with an integrated coding agent, accessible from any directory via the `jarvis` command.

## Features

- **Voice-first interface** — speak naturally, get spoken responses
- **Sleep mode** — global hotkey (`Ctrl+Shift+M`) toggles the mic on/off
- **Query classification** — Cohere-powered intent detection routes queries to the right engine
- **Real-time search** — Tavily + BeautifulSoup web search with dual-key round-robin
- **Conversation AI** — Groq-powered chat with primary/fallback model chain
- **Text-to-speech** — edge-tts with ffplay playback (output suppressed)
- **Speech-to-text** — Selenium + Chrome Web Speech API
- **Coding agent** — AI coding assistant with multi-provider support, file operations, and project awareness
- **Multi-provider routing** — each module can use a different provider/model

## Architecture

```
Ultimate-Jarvs/
├── Main.py                 # Voice assistant entry point (jarvis)
├── jarvis.bat              # Windows wrapper — runs from any terminal
├── Backend/
│   ├── Model.py            # Query classifier (Cohere)
│   ├── Chatbot.py          # Conversation engine (Groq)
│   ├── RealtimeSearchEngine.py  # Web search (Tavily + BS4 + Groq)
│   ├── SpeechToText.py     # Voice input (Chrome Web Speech API)
│   ├── TextToSpeech.py     # Speech output (edge-tts + ffplay)
│   ├── MicControl.py       # Global hotkey mic toggle
│   └── ImageGeneration.py  # Image generation
├── Coding_agent/           # AI coding assistant
│   ├── cli.py              # Terminal interface (opencode-style `>` prompt)
│   ├── agentic_ai.py       # Session orchestrator
│   ├── providers.py        # Multi-provider client registry
│   ├── workflow.py         # File operation tools
│   ├── query_explainer.py  # Intent classification
│   ├── Reasoning.py        # Solution architecture
│   ├── Code_gen.py         # Code generation
│   ├── editing.py          # File editing
│   ├── debugger.py         # Bug analysis + fixes
│   ├── asking.py           # Clarifying questions
│   ├── gen_ai.py           # General Q&A
│   ├── colaborator.py      # Multi-file coordination
│   ├── knowledge.py        # Tech stack reference context
│   └── knowledge/          # Pattern libraries (7 tech domains)
├── Data/                   # Chat history (ChatLog.json)
├── Frontend/               # IPC state files
└── .env                    # API keys and configuration
```

## Quick Start

### Prerequisites

- Python 3.10+
- [Google Chrome](https://www.google.com/chrome/) (for speech-to-text)
- [ffplay](https://ffmpeg.org/) (for text-to-speech, part of FFmpeg)

### Installation

```bash
# Clone or navigate to the project
cd ULTRON

# Create a virtual environment
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r Requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and fill in your API keys:

| Variable | Required | Description |
|---|---|---|
| `CohereAPIKey` | Yes | Query classification |
| `GroqAPIKey` | Yes | General conversation + search |
| `TavilyAPIKey1` | Yes | Web search (primary key) |
| `TavilyAPIKey2` | No | Web search (fallback, round-robin) |
| `OpenRouterAPIKey1-6` | For coding | Coding agent LLM (6 keys, round-robin) |
| `Username` | Yes | Your name for the UI |
| `Assistantname` | Yes | Assistant name displayed |

### Run

```bash
# Voice assistant
python Main.py

# Or from any terminal (after adding ULTRON to PATH)
jarvis
```

### Coding Agent

The coding agent launches automatically from the voice assistant when it detects a coding-related query. It provides an interactive terminal (`>` prompt) with:

- **Natural language** — describe what to build, edit, or debug
- **File operations** — `/read`, `/write`, `/list`, `/delete`, `/analyze`
- **Project awareness** — detects tech stack and provides relevant patterns

## Usage

### Voice Commands

| Say... | What happens |
|---|---|
| "What's the weather?" | Real-time search + spoken response |
| "Create a React component" | Launches the coding agent |
| "Tell me about X" | General conversation |
| "Exit" / "Quit" / "Bye" | Ends the session |

### Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+Shift+M` | Toggle microphone (sleep/wake) |
| `Ctrl+C` | Exit the assistant |

### Coding Agent Commands

| Command | Description |
|---|---|
| `create a REST API with FastAPI` | Generate code from natural language |
| `/read path/to/file` | Display file contents |
| `/write path/to/file` | Write content to a file |
| `/list [dir]` | List files in a directory |
| `/delete path/to/file` | Delete a file |
| `/analyze path/to/file` | Show file statistics |
| `/exit` | Return to voice assistant |

## Provider Architecture

The system uses multiple LLM providers, each with role-specific routing:

| Module | Provider | Model |
|---|---|---|
| Query classification | Cohere | `command-r-plus` |
| General conversation | Groq | `llama-3.3-70b-versatile` (fallback: `llama-3.1-8b-instant`) |
| Web search synthesis | Groq | `llama-3.1-8b-instant` (fallback: `llama-3.3-70b-versatile`) |
| Coding: orchestrator | OpenRouter | `deepseek/deepseek-chat` |
| Coding: explainer | Groq | `llama-3.3-70b-versatile` |
| Coding: reasoning | OpenRouter | `deepseek/deepseek-r1` |
| Coding: code gen | OpenRouter | `qwen/qwen-2.5-coder-32b-instruct` |
| Coding: editing | OpenRouter | `qwen/qwen-2.5-coder-32b-instruct` |
| Coding: debugger | Groq | `llama-3.3-70b-versatile` |

All providers use OpenAI-compatible API format via the `openai` library.

## Environment Variables

See `.env.example` for the full list. Key configuration:

- **`CohereModel`** — Classification model (default: `command-r-plus-08-2024`)
- **`GroqChatModel`** — Primary conversation model
- **`GroqChatFallback`** — Fallback when primary is unavailable
- **`GroqSearchModel`** — Search synthesis model
- **`CodingGroqAPIKey`** — Falls back to `GroqAPIKey` if not set
- **`InputLanguage`** — Speech recognition language (e.g., `en, hi`)
- **`AssistantVoice`** — TTS voice (e.g., `en-CA-LiamNeural`)
- **`Agent*`** — Per-module model overrides for the coding agent

## Coding Agent Knowledge

The coding agent includes reference pattern libraries for 7 technology domains:

- **Python** — FastAPI, SQLAlchemy, pytest, asyncio
- **React** — Hooks, routing, state management, testing
- **JavaScript** — ES6+, async/await, DOM APIs, testing
- **Node.js** — Express, Prisma, auth, deployment
- **TypeScript** — Advanced types, React+TS, config
- **HTML/CSS** — Semantic markup, Flexbox, Grid, Tailwind
- **Database** — SQL, ORMs (SQLAlchemy, Prisma, Mongoose), schema design

When generating code, the agent loads relevant patterns as context to produce idiomatic, best-practice code.

## Credits

Developped by **`Naitik!!`**
