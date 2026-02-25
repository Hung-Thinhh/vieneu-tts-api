# VieNeu TTS API Documentation

Hệ thống API chuyển đổi văn bản thành giọng nói (TTS) tiếng Việt sử dụng mô hình GGUF siêu nhẹ, tối ưu cho CPU.

## 🚀 Khởi động nhanh (Quick Start)

API Server chạy mặc định tại cổng `8000`.

### Địa chỉ endpoint (Production):
`https://tenmiencuaban.com/tts`

---

## 🛠 Các Endpoint API

### 1. [POST] Tạo giọng nói từ văn bản
**URL:** `/tts`

**Request Body (JSON):**
| Tham số | Kiểu | Mô tả | Mặc định |
|---|---|---|---|
| `text` | string | (BẮT BUỘC) Văn bản cần đọc. | |
| `voice_id` | string | ID của giọng nói (xem danh sách bên dưới). | `Doan` |

**Ví dụ (Postman/cURL):**
```json
{
    "text": "Chào bạn, đây là ví dụ về gọi API giọng nữ miền Nam.",
    "voice_id": "Doan"
}
```

**Response:** File âm thanh định dạng `.wav` (binary).

---

### 2. [GET] Danh sách giọng nói
**URL:** `/voices`

**Response:**
Trả về danh sách các `voice_id` và mô tả chi tiết:
- `Doan`: Nữ miền Nam ⭐ (Mặc định)
- `Vinh`: Nam miền Nam
- `Ly`: Nữ miền Bắc
- `Ngoc`: Nữ miền Bắc (2)
- `Binh`: Nam miền Bắc
- `Tuyen`: Nam miền Bắc (2)

---

## 💻 Ví dụ Code gọi API (Python)

```python
import requests

def text_to_speech(text, voice="Doan", output_file="output.wav"):
    url = "https://vieneutts.dukyai.com/tts"
    payload = {
        "text": text,
        "voice_id": voice
    }
    
    print(f"⏳ Đang xử lý: {text[:30]}...")
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"✅ Đã lưu file: {output_file}")
    else:
        print(f"❌ Lỗi: {response.status_code}")
        print(response.text)

# Chạy thử
text_to_speech("Xin chào bạn, chúc bạn một ngày tốt lành!", voice="Doan")
```

---

## ⚙️ Cấu hình hệ thống (Dành cho Admin)

### Chạy trực tiếp trên Host:
```bash
cd /root/VieNeu-TTS
PYTHONPATH=src .venv/bin/python run_api_server.py
```

### Triển khai qua Docker (Dokploy/Traefik):
Dùng file `docker-compose.yml` có sẵn để proxy traffic từ Traefik vào port 23333 trên host qua `socat`.

---
*VieNeu-TTS API - Optimized by Antigravity AI*
