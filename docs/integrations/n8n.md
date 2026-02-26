# N8N Integration สำหรับ memU

คู่มืออ้างอิงฉบับสมบูรณ์สำหรับการเชื่อมต่อ memU กับ N8N

## สถาปัตยกรรม (Architecture)

```
LINE User
    │
    ▼
LINE Platform
    │  (HTTPS Webhook)
    ▼
N8N Workflow Engine
    │
    ├──[1] HTTP Request: POST /retrieve
    │         │
    │         ▼
    │    memU API Server (FastAPI)
    │         │
    │         ▼
    │    memU MemoryService
    │         │
    │         ├── in-memory (dev)
    │         └── PostgreSQL (prod)
    │
    ├──[2] OpenAI Chat Node
    │         │
    │         ▼
    │    OpenAI API (gpt-4o-mini)
    │
    ├──[3] HTTP Request: POST /memorize
    │         │
    │         ▼
    │    memU API Server
    │
    └──[4] LINE Reply
              │
              ▼
         LINE User
```

## API Endpoint Specifications

Base URL: `http://localhost:8001` (ปรับได้ตาม deployment)

---

### GET /health

ตรวจสอบสถานะของ memU API Server

**Response:**
```json
{
  "status": "ok",
  "service": "memU API"
}
```

---

### POST /memorize

บันทึกข้อความหรือการสนทนาลง memU

**Request Body:**
```json
{
  "user_id": "user123",
  "text": "ข้อความที่ต้องการบันทึก",
  "modality": "conversation"
}
```

| Field | Type | Required | คำอธิบาย |
|-------|------|----------|----------|
| `user_id` | string | ✅ | รหัสผู้ใช้ที่ไม่ซ้ำกัน |
| `text` | string | ✅ | เนื้อหาที่ต้องการบันทึก |
| `modality` | string | ❌ | ประเภทข้อมูล (default: `conversation`) |

**Response:**
```json
{
  "status": "ok",
  "user_id": "user123",
  "items_count": 3
}
```

---

### POST /retrieve

ค้นหาความทรงจำที่เกี่ยวข้องกับคำถาม

**Request Body:**
```json
{
  "user_id": "user123",
  "text": "ผู้ใช้ชอบอะไร?"
}
```

| Field | Type | Required | คำอธิบาย |
|-------|------|----------|----------|
| `user_id` | string | ✅ | รหัสผู้ใช้ |
| `text` | string | ✅ | คำถามหรือ query สำหรับค้นหา |

**Response:**
```json
{
  "status": "ok",
  "user_id": "user123",
  "items": [
    {
      "summary": "ผู้ใช้ชอบกาแฟดำและโปรแกรมมิ่ง",
      "score": 0.92
    }
  ],
  "context": "ผู้ใช้ชอบกาแฟดำและโปรแกรมมิ่ง"
}
```

---

### GET /categories/{user_id}

ดึงรายการหมวดหมู่ความทรงจำทั้งหมดของผู้ใช้

**Path Parameter:**
- `user_id`: รหัสผู้ใช้

**Response:**
```json
{
  "status": "ok",
  "user_id": "user123",
  "categories": [
    {
      "name": "preferences",
      "summary": "ผู้ใช้ชอบกาแฟดำ, Dark mode"
    },
    {
      "name": "personal_info",
      "summary": "ชื่อ: สมชาย, อายุ: 30 ปี"
    }
  ]
}
```

---

### DELETE /memory/{user_id}

ลบความทรงจำทั้งหมดของผู้ใช้

**Path Parameter:**
- `user_id`: รหัสผู้ใช้

**Response:**
```json
{
  "status": "ok",
  "user_id": "user123",
  "deleted": 15
}
```

---

## การตั้งค่า N8N Nodes

### HTTP Request Node (Retrieve Memory)

```
Method: POST
URL: http://localhost:8001/retrieve
Body (JSON):
{
  "user_id": "{{ $json.userId }}",
  "text": "{{ $json.messageText }}"
}
```

### HTTP Request Node (Memorize)

```
Method: POST
URL: http://localhost:8001/memorize
Body (JSON):
{
  "user_id": "{{ $json.userId }}",
  "text": "User: {{ $json.messageText }}\nAssistant: {{ $json.replyText }}",
  "modality": "conversation"
}
```

### OpenAI Chat Node

```
Model: gpt-4o-mini
System Prompt:
  คุณเป็นผู้ช่วย AI ที่ฉลาดและเป็นมิตร
  คุณมีความทรงจำเกี่ยวกับผู้ใช้ดังนี้:

  {{ $json.memoryContext }}

  ใช้ข้อมูลนี้ในการตอบคำถามและสนทนากับผู้ใช้
```

---

## Security (ความปลอดภัย)

### API Key Authentication (แนะนำสำหรับ production)

เพิ่ม API key authentication ด้วยการตั้งค่า environment variable และตรวจสอบใน middleware:

```python
# ใน memu_api_server.py (เพิ่มเอง)
from fastapi import Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != os.getenv("API_SECRET_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API Key")
```

จากนั้นตั้ง Header ใน N8N HTTP Request nodes:
```
Header: X-API-Key: your-secret-key
```

### Network Security

- ใช้ HTTPS สำหรับ production (ผ่าน nginx/Caddy reverse proxy)
- จำกัด IP ที่เข้าถึงได้ด้วย firewall rules
- ไม่ expose memU API Server โดยตรงสู่ internet (ให้ N8N เป็น gateway)

---

## Deployment Options

### 1. Local Development

```bash
cd examples/n8n
uvicorn memu_api_server:app --host 0.0.0.0 --port 8001 --reload
```

### 2. Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY examples/n8n/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install memu
COPY examples/n8n/memu_api_server.py .
CMD ["uvicorn", "memu_api_server:app", "--host", "0.0.0.0", "--port", "8001"]
```

```bash
docker build -t memu-api .
docker run -p 8001:8001 \
  -e OPENAI_API_KEY=sk-... \
  -e DATABASE_URL=postgresql://... \
  memu-api
```

### 3. Cloud (Render, Railway, Fly.io)

ตัวอย่างสำหรับ **Render**:
1. สร้าง Web Service ใหม่
2. ตั้ง Build Command: `pip install -r examples/n8n/requirements.txt && pip install -e .`
3. ตั้ง Start Command: `uvicorn examples.n8n.memu_api_server:app --host 0.0.0.0 --port $PORT`
4. เพิ่ม Environment Variables: `OPENAI_API_KEY`, `DATABASE_URL`

---

## Workflows

### line_memu_bot.json

LINE Chatbot ที่มีความทรงจำ - ทำงานตาม flow:

1. **LINE Webhook** - รับ event จาก LINE Platform
2. **Parse LINE Event** - ดึง `userId`, `replyToken`, `messageText`
3. **Retrieve Memory** - ดึงความทรงจำที่เกี่ยวข้องจาก memU
4. **Build Memory Context** - สร้าง context string จากความทรงจำ
5. **OpenAI Chat** - สร้างคำตอบโดยใช้ความทรงจำเป็น context
6. **Extract AI Reply** - ดึงข้อความตอบกลับจาก OpenAI
7. **Memorize Conversation** - บันทึกการสนทนาลง memU
8. **LINE Reply** - ส่งคำตอบกลับไปยังผู้ใช้
9. **Webhook Response** - ส่ง 200 OK กลับให้ LINE Platform

### memory_dashboard.json

สรุปความทรงจำรายวัน - ทำงานทุกวันเวลา 08:00:

1. **Schedule at 08:00** - trigger ตาม cron `0 8 * * *`
2. **Set User ID** - กำหนด user_id ที่ต้องการ
3. **Get Memory Categories** - ดึงหมวดหมู่ความทรงจำจาก memU
4. **Format Summary** - จัดรูปแบบข้อความสรุป
5. **LINE Push Summary** - ส่งสรุปไปยัง LINE
