from vieneu import Vieneu
import os

print("⏳ Khởi tạo VieNeu TTS model (Phiên bản GGUF siêu nhẹ)...")
tts = Vieneu(
    mode='standard', 
    backbone_repo="pnnbao-ump/VieNeu-TTS-0.3B-q4-gguf",
    backbone_device="cpu", 
    codec_repo="neuphonic/neucodec-onnx-decoder-int8", 
    codec_device="cpu"
)

os.makedirs("outputs", exist_ok=True)

# Lấy giọng nói mặc định có sẵn
voice_data = tts.get_preset_voice(None)

text_to_speak = "anh Thịnh ơi, em fan anh hú hú"

print(f"🎙 Đang tạo âm thanh cho văn bản: '{text_to_speak}'")
print("⏳ Vui lòng đợi trong giây lát, quá trình có thể mất từ 10-30 giây tùy tốc độ CPU...")

# Generate audio (non-streaming)
audio_spec = tts.infer(text=text_to_speak, voice=voice_data)

output_path = "outputs/standard_output.wav"
tts.save(audio_spec, output_path)

print(f"✅ Đã tạo xong! File âm thanh được lưu tại: {os.path.abspath(output_path)}")
print("   - Bạn có thể copy file này qua máy cá nhân để nghe thử.")

tts.close()
