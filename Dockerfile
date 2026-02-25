FROM python:3.11-slim

# Cài đặt espeak-ng (dependency của VieNeu-TTS)
RUN apt-get update && apt-get install -y espeak-ng && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY src/ src/
COPY run_api_server.py .
COPY apps/ apps/

# Cài uv và dependencies
RUN pip install uv && uv sync

EXPOSE 8000

CMD ["uv", "run", "python", "run_api_server.py"]
