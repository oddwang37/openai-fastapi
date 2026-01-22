server:
    uv run uvicorn app.main:app --reload
test:
    pytest
lint:
    ruff check
    ruff format
use_ollama:
    cp .env.ollama .env
    ollama run llama2
use_openai:
    cp .env.openai .env
