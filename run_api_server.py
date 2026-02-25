from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import Optional
import uvicorn
from vieneu import Vieneu
import tempfile
import os

app = FastAPI(title="VieNeu TTS API", description="API tạo giọng nói từ văn bản")

print("⏳ Khởi tạo VieNeu TTS model (Phiên bản GGUF siêu nhẹ)...")
tts = Vieneu(
    mode='standard', 
    backbone_repo="pnnbao-ump/VieNeu-TTS-0.3B-q4-gguf",
    backbone_device="cpu", 
    codec_repo="neuphonic/neucodec-onnx-decoder-int8", 
    codec_device="cpu"
)

# Cache tất cả giọng vào RAM khi khởi động để không tải lại mỗi request
VOICES = {
    "Binh":  tts.get_preset_voice("Binh"),   # nam miền Bắc
    "Tuyen": tts.get_preset_voice("Tuyen"),  # nam miền Bắc
    "Vinh":  tts.get_preset_voice("Vinh"),   # nam miền Nam
    "Doan":  tts.get_preset_voice("Doan"),   # nữ miền Nam ⭐
    "Ly":    tts.get_preset_voice("Ly"),     # nữ miền Bắc
    "Ngoc":  tts.get_preset_voice("Ngoc"),   # nữ miền Bắc
}
DEFAULT_VOICE = "Doan"
print(f"✅ Server API đã sẵn sàng! Các giọng có sẵn: {list(VOICES.keys())}")

class TTSRequest(BaseModel):
    text: str
    voice_id: Optional[str] = DEFAULT_VOICE  # Mặc định: Doan (nữ miền Nam)

@app.post("/tts")
async def generate_tts(request: TTSRequest):
    voice_key = request.voice_id if request.voice_id in VOICES else DEFAULT_VOICE
    print(f"🎙 Giọng: {voice_key} | Văn bản: '{request.text[:60]}...'")
    
    voice_data = VOICES[voice_key]
    audio_spec = tts.infer(text=request.text, voice=voice_data)
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        tmp_path = f.name
        
    tts.save(audio_spec, tmp_path)
    
    with open(tmp_path, "rb") as f:
        wav_data = f.read()
        
    os.remove(tmp_path)
    
    print("✅ Đã trả về file âm thanh thành công.")
    return Response(content=wav_data, media_type="audio/wav")

@app.get("/voices")
def list_voices():
    """Danh sách giọng nói có sẵn"""
    return {
        "voices": {
            "Binh":  "Nam miền Bắc",
            "Tuyen": "Nam miền Bắc (2)",
            "Vinh":  "Nam miền Nam",
            "Doan":  "Nữ miền Nam ⭐ (mặc định)",
            "Ly":    "Nữ miền Bắc",
            "Ngoc":  "Nữ miền Bắc (2)",
        },
        "default": DEFAULT_VOICE
    }

@app.get("/")
def read_root():
    return {
        "message": "VieNeu TTS API đang chạy.",
        "docs": "Gửi POST tới /tts với body: {\"text\": \"...\", \"voice_id\": \"Doan\"}",
        "voices": "/voices"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
