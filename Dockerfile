# CONCEPT: containerising the API so it runs the same on your laptop and on AWS.
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
COPY knowledge ./knowledge
COPY data/raw ./data/raw
RUN uv sync --frozen --no-dev
EXPOSE 8000
CMD ["uv", "run", "--no-dev", "uvicorn", "energy_agent.api:app", "--host", "0.0.0.0", "--port", "8000"]
