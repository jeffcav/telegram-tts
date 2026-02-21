# Dockerfile for Telegram-TTS Backend
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


# Download Kokoro TTS model during build
RUN mkdir -p kokoro_model \
	&& echo "Downloading Kokoro TTS model..." \
	&& wget -O kokoro_model/model.pth https://github.com/kokoro-ai/kokoro-tts/releases/latest/download/model.pth || true


# Copy backend code
COPY app.py ./

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
