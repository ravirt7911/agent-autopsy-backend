# Agent Diagnostic Backend

A FastAPI-based backend service for diagnosing AI agent failures. This system analyzes agent execution traces and identifies the primary structural failure that caused the agent to fail or underperform.

## Project Structure

```
agent-diagnostic-backend/
├── app/                    # Main application package
│   ├── __init__.py        # Package initialization
│   ├── main.py            # FastAPI application setup
│   ├── config.py          # Configuration management
│   ├── prompts.py         # LLM prompt templates
│   ├── api/               # API routes
│   │   ├── __init__.py
│   │   └── routes.py      # Endpoint handlers
│   ├── core/              # Core business logic
│   │   ├── __init__.py
│   │   └── diagnostic_engine.py  # Diagnostic analysis engine
│   └── models/            # Data models
│       ├── __init__.py
│       └── schemas.py     # Pydantic models
├── run.py                 # Application entry point
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Architecture

### Package Organization

- **`app/api/`**: Contains all API route handlers and endpoints
- **`app/core/`**: Contains core business logic (diagnostic engine)
- **`app/models/`**: Contains Pydantic data models for requests/responses
- **`app/config.py`**: Centralized configuration management using environment variables
- **`app/prompts.py`**: LLM prompt templates and builders
- **`app/main.py`**: FastAPI application initialization and middleware setup

### Key Components

1. **Diagnostic Engine** (`app/core/diagnostic_engine.py`): 
   - Analyzes agent failures using OpenAI's API
   - Implements retry logic and error handling
   - Validates LLM responses

2. **API Routes** (`app/api/routes.py`):
   - `/` - Health check endpoint
   - `/health` - Simple health check
   - `/diagnose` - Main diagnostic endpoint (POST)

3. **Configuration** (`app/config.py`):
   - Centralized settings management
   - Environment variable loading
   - Configuration validation

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your configuration:
```env
OPENAI_API_KEY=your_api_key_here
PORT=8000
HOST=0.0.0.0
OPENAI_MODEL=gpt-5.2-2025-12-11
OPENAI_TEMPERATURE=0.3
CORS_ORIGINS=*
```

3. Run the application:
```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### POST `/diagnose`

Analyzes an agent failure and returns a diagnosis.

**Request Body:**
```json
{
  "agent_goal": "What the agent was supposed to accomplish",
  "instructions": "The instructions or system prompt given to the agent",
  "execution_steps": "The steps the agent took, including tool calls and reasoning",
  "final_output": "The final output produced by the agent",
  "expected_output": "Optional: What the output should have been"
}
```

**Response:**
```json
{
  "verdict": "The primary failure type identified",
  "explanation": "Plain English explanation of what went wrong",
  "evidence": ["Specific examples from the execution"],
  "recommended_fix": "One clear, actionable recommendation",
  "confidence": "high, medium, or low"
}
```

### GET `/health`

Simple health check endpoint.

### GET `/`

Health check with version information.

## Development

The codebase follows a clean architecture pattern with clear separation of concerns:

- **API Layer**: Handles HTTP requests/responses
- **Core Layer**: Contains business logic
- **Models Layer**: Defines data structures
- **Config Layer**: Manages application configuration

All imports use absolute imports from the `app` package for clarity and maintainability.

# agent-autopsy-backend
