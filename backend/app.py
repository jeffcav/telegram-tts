import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import FileResponse
import tempfile

# Kokoro TTS import (placeholder, update if needed)
try:
    from kokoro_tts import KokoroTTS
except ImportError:
    KokoroTTS = None

app = FastAPI()

# Path to local Kokoro TTS model directory
MODEL_PATH = os.path.join(os.path.dirname(__file__), "kokoro_model")

# Load Kokoro TTS model at startup
if KokoroTTS:
    tts_engine = KokoroTTS(model_path=MODEL_PATH)
else:
    tts_engine = None

class TTSRequest(BaseModel):
    text: str

@app.post("/tts")
def tts_endpoint(request: TTSRequest):
    if not tts_engine:
        raise HTTPException(status_code=500, detail="Kokoro TTS not available.")
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text input required.")
    try:
        # Generate audio file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
            tts_engine.synthesize_to_file(request.text, tmp_audio.name)
            tmp_audio_path = tmp_audio.name
        return FileResponse(tmp_audio_path, media_type="audio/wav", filename="output.wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")
