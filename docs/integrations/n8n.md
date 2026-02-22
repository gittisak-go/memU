# N8N Integration

> เชื่อม **memU** กับ **N8N** เพื่อสร้าง AI Agent ที่มีหน่วยความจำระยะยาวแบบ no-code

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      N8N Workflow                           │
│                                                             │
│  Trigger → HTTP Request → Code Node → HTTP Request → ...   │
│              (retrieve)               (memorize)           │
└─────────────────────────────────────────────────────────────┘
                │                          │
                ▼                          ▼
        ┌───────────────────────────────────────┐
        │           memU API Server             │
        │         (FastAPI / uvicorn)            │
        │                                       │
        │  POST /memorize   POST /retrieve       │
        │  GET  /categories DELETE /memory       │
        │  GET  /health                         │
        └───────────────────────────────────────┘
                          │
                          ▼
                ┌─────────────────┐
                │   memU Memory   │
                │     Store       │
                │ (SQLite / PG /  │
                │  In-Memory)     │
                └─────────────────┘
```

---

## ไฟล์ที่เกี่ยวข้อง

| ไฟล์ | คำอธิบาย |
|---|---|
| `examples/n8n/memu_api_server.py` | FastAPI server หลัก |
| `examples/n8n/requirements.txt` | Python dependencies |
| `examples/n8n/.env.example` | ตัวอย่าง environment variables |
| `examples/n8n/workflows/line_memu_bot.json` | N8N workflow: LINE Bot |
| `examples/n8n/workflows/memory_dashboard.json` | N8N workflow: Daily Summary |
| `examples/n8n/README.md` | คู่มือภาษาไทยฉบับสมบูรณ์ |

---

## API Endpoint Reference

### `GET /health`

ตรวจสอบว่า server ทำงานอยู่

**Response:**
```json
{ "status": "ok", "service": "memU API for N8N" }
```

---

### `POST /memorize`

บันทึกข้อความลงใน memU memory store

**Request Body:**
```json
{
  "user_id": "string",
  "text": "string",
  "modality": "conversation"
}
```

**Response:**
```json
{
  "success": true,
  "user_id": "string",
  "result": {
    "items": [...],
    "categories": [...]
  }
}
```

---

### `POST /retrieve`

ค้นหาความจำที่เกี่ยวข้องกับ query

**Request Body:**
```json
{
  "user_id": "string",
  "text": "string",
  "modality": "conversation"
}
```

**Response:**
```json
{
  "success": true,
  "user_id": "string",
  "memory_context": "- ข้อมูล 1\n- ข้อมูล 2",
  "items": [
    {
      "id": "uuid",
      "summary": "string",
      "memory_type": "profile | event | knowledge | behavior"
    }
  ],
  "raw": {...}
}
```

> **หมายเหตุ:** ใช้ `memory_context` ใส่ใน system prompt ของ LLM node ใน N8N

---

### `GET /categories`

ดึงรายการ memory categories ของ user

**Query Parameters:**
- `user_id` (required) — user identifier

**Response:**
```json
{
  "success": true,
  "user_id": "string",
  "categories": [
    {
      "id": "uuid",
      "name": "preferences",
      "summary": "ชอบกินข้าวผัดกุ้ง ไม่ชอบผักชี"
    }
  ]
}
```

---

### `DELETE /memory`

ลบความจำทั้งหมดของ user

**Request Body:**
```json
{ "user_id": "string" }
```

**Response:**
```json
{
  "success": true,
  "user_id": "string",
  "cleared": {
    "deleted_categories": [...],
    "deleted_items": [...],
    "deleted_resources": [...]
  }
}
```

---

## N8N Node Configuration

### HTTP Request Node — POST /retrieve

| Field | Value |
|---|---|
| Method | POST |
| URL | `{{ $env.MEMU_API_URL }}/retrieve` |
| Body Type | JSON |
| Body | `{"user_id": "{{ $json.userId }}", "text": "{{ $json.userMessage }}"}` |

### HTTP Request Node — POST /memorize

| Field | Value |
|---|---|
| Method | POST |
| URL | `{{ $env.MEMU_API_URL }}/memorize` |
| Body Type | JSON |
| Body | `{"user_id": "{{ $json.userId }}", "text": "{{ $json.text }}"}` |

### N8N Environment Variables

ตั้งค่าใน N8N Settings → Variables:

| Variable | คำอธิบาย |
|---|---|
| `MEMU_API_URL` | URL ของ memU API Server เช่น `http://localhost:8000` |
| `LINE_CHANNEL_ACCESS_TOKEN` | LINE Channel Access Token |
| `DASHBOARD_USER_ID` | LINE User ID สำหรับ daily summary |

---

## Security และ Deployment

### การรักษาความปลอดภัย

1. **ไม่ expose memU API โดยตรงบน internet** — วาง reverse proxy (nginx/Caddy) ไว้หน้า หรือให้เข้าถึงได้เฉพาะ N8N
2. **ใช้ HTTPS** สำหรับ LINE Webhook URL (LINE กำหนด)
3. **เก็บ keys ใน environment variables** — ไม่ hardcode ใน workflow
4. **ใช้ N8N Credentials system** สำหรับ LINE และ OpenAI credentials

### การ Deploy บน Production

```bash
# รัน API Server ด้วย uvicorn
uvicorn memu_api_server:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 2

# ตั้งค่า SQLite เพื่อ persist ข้อมูล
export DATABASE_URL=sqlite:///./data/memu.db
```

### Docker Compose ตัวอย่าง

```yaml
version: "3.8"
services:
  memu-api:
    build: ./examples/n8n
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=sqlite:///./data/memu.db
    volumes:
      - memu_data:/app/data
    ports:
      - "8000:8000"

  n8n:
    image: n8nio/n8n
    environment:
      - N8N_VAR_MEMU_API_URL=http://memu-api:8000
      - N8N_VAR_LINE_CHANNEL_ACCESS_TOKEN=${LINE_CHANNEL_ACCESS_TOKEN}
    ports:
      - "5678:5678"

volumes:
  memu_data:
```

---

## ข้อจำกัดและหมายเหตุ

- **In-memory store (default)** — ข้อมูลจะหายเมื่อ restart server ควรตั้งค่า `DATABASE_URL` สำหรับ production
- **Concurrent requests** — MemoryService ใช้ async Python, N8N สามารถเรียก endpoint พร้อมกันได้หลาย request
- **Cold start** — การเรียก `/memorize` ครั้งแรกจะช้ากว่าปกติเนื่องจาก LLM client initialization
- **ไม่ได้ duplicate กับ `examples/line_bot/`** — N8N integration เน้น no-code layer ผ่าน HTTP API ส่วน `line_bot` เป็น Python SDK โดยตรง
