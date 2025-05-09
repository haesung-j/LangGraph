[English](README.en.md) | [한국어](README.ko.md)

# Meta-Prompt Generator

An interactive prompt generation chatbot utilizing LangGraph, designed to create optimized prompts through user conversations.

<img src="https://github.com/user-attachments/assets/69072c0f-8d8d-421d-83b2-298b6ae82fec">

## Key Features

- LLM-based interactive meta-prompt generation and optimization
- Real-time streaming responses using Server-Sent Events (SSE)
- Responsive web interface built with Streamlit

## Architecture

![System Architecture](graph.png)

This diagram shows the state-based workflow of the system:
1. **Information Gathering**: Collection and analysis of user requirements
2. **Tool Message Processing**: Intermediate processing and state updates
3. **Prompt Generation**: Creation of optimized meta-prompts

## Tech Stack

- 🐍 Python 3.11+ (supports type hinting and modern async features)
- ⚡ FastAPI (async API endpoints and SSE streaming)
- 🔄 LangGraph (state-based workflow management)
- 🦜 LangChain (LLM integration and prompt management)
- 🎈 Streamlit (interactive web interface)
- 🐳 Docker (containerization and deployment)

## Getting Started

### Running Locally

1. Install uv package manager
```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Set up the project
```bash
# Clone the repository
git clone https://github.com/haesung-j/meta-prompt.git
cd meta-prompt

# Create virtual environment and install dependencies
uv python install 3.11
uv venv --python=3.11
uv sync

# Set up environment variables
cp .env.example .env
# Edit the .env file to set the required API keys
```

3. Run the server
```bash
bash start.sh
```

### Running with Docker

```bash
# Build the image
docker build -t meta-prompt .

# Run the container (pay attention to mapped ports)
docker run -p 8501:8501 --name meta-prompt meta-prompt
```

## How to Use

1. Access `http://localhost:8501` in your web browser
2. Input your prompt generation requirements in the chat interface
   - Describe the purpose of the prompt
   - Define necessary variables
   - Set output constraints
3. Review and provide feedback on the generated prompt in real-time
4. Copy the final prompt for use

## API Endpoints

- GET `/chat/stream`: Streaming chat API (SSE-based)
  - Parameters:
    - `query`: User input text (required)
    - `thread_id`: Chat thread ID (optional, default is auto-generated)
  - Response: Streaming response in `text/event-stream` format

## Environment Variables

You need to set the following environment variables in the `.env` file:

```
OPENAI_API_KEY=your_openai_api_key  # your_openai_api_key # OpenAI API key (required)
MODEL_NAME=gpt-4o                   # Model to use (default: gpt-4o)
TEMPERATURE=0.7                     # Generation diversity setting (0.0-1.0)
```