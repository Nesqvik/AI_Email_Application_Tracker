FROM python:3.11-slim
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY . .
EXPOSE 8501
CMD ["uv", "run", "streamlit", "run", "email_check_app.py", "--server.address=0.0.0.0"]