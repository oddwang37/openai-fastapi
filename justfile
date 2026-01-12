server:
    uv run uvicorn app.main:app --reload
test:
    pytest
lint:
    ruff check
    ruff format
