# N8N Integration

เอกสารอ้างอิงสำหรับการเชื่อม **memU** กับ **N8N** workflow automation

---

## ภาพรวม

N8N + memU ช่วยให้ผู้ใช้ไทยสามารถสร้าง AI Agent ที่มีหน่วยความจำระยะยาวได้โดยไม่ต้องเขียนโค้ด โดย memU API server ทำหน้าที่เป็น HTTP backend ที่ N8N เรียกผ่าน HTTP Request node

### สถาปัตยกรรม

```
LINE User
   │
   ▼
LINE Platform
   │  Webhook
   ▼
N8N Workflow
   │                    │
   ▼                    ▼
POST /retrieve      POST /memorize
   │                    │
   └──── memU API ───────┘
              │
              ▼
         OpenAI / LLM
              │
              ▼
       LINE Reply API
```

---

## API Endpoint Reference

Base URL: `http://localhost:8001` (ปรับตาม deployment ของคุณ)

### GET /health

ตรวจสอบสถานะ API server

**Response:**
```json
{"status": "ok", "service": "memU API for N8N"}
```

---

### POST /memorize

บันทึกข้อความหรือบทสนทนาลงหน่วยความจำของ user

**Request Body:**
```json
{
  "user_id": "line_uid_xxx",
  "text": "ข้อความที่ต้องการบันทึก",
  "modality": "conversation"
}
```

| Field | Type | คำอธิบาย |
|-------|------|-----------|
| `user_id` | string | LINE User ID หรือ identifier ของผู้ใช้ |
| `text` | string | ข้อความที่ต้องการบันทึก |
| `modality` | string | ประเภทข้อมูล: `conversation`, `document`, `log` |

**Response:**
```json
{
  "status": "ok",
  "user_id": "line_uid_xxx",
  "items_stored": 3,
  "categories": 2
}
```

---

### POST /retrieve

ดึงความจำที่เกี่ยวข้องกับ query ของ user

**Request Body:**
```json
{
  "user_id": "line_uid_xxx",
  "text": "คำถามหรือบริบทที่ต้องการค้นหา",
  "modality": "conversation"
}
```

**Response:**
```json
{
  "status": "ok",
  "user_id": "line_uid_xxx",
  "summary": "สรุปความจำที่เกี่ยวข้อง...",
  "memories": [
    {
      "id": "mem-xxx",
      "summary": "ผู้ใช้ชอบกาแฟอเมริกาโน่",
      "memory_type": "preferences"
    }
  ],
  "count": 1
}
```

ใช้ `summary` เป็น context ส่งให้ OpenAI เพื่อสร้างคำตอบ

---

### GET /categories

ดูหมวดหมู่ความจำทั้งหมดของ user

**Query Parameter:** `user_id=line_uid_xxx`

**Response:**
```json
{
  "status": "ok",
  "user_id": "line_uid_xxx",
  "categories": [
    {
      "id": "cat-xxx",
      "name": "preferences",
      "summary": "ผู้ใช้ชอบกาแฟ ชอบสีฟ้า..."
    }
  ]
}
```

---

### DELETE /memory

ลบความจำทั้งหมดของ user

**Request Body:**
```json
{
  "user_id": "line_uid_xxx"
}
```

**Response:**
```json
{
  "status": "ok",
  "user_id": "line_uid_xxx",
  "message": "ลบความจำของ line_uid_xxx เรียบร้อยแล้ว"
}
```

---

## N8N Node Configuration Guide

### HTTP Request Node — POST /memorize

| Field | ค่า |
|-------|-----|
| Method | `POST` |
| URL | `http://localhost:8001/memorize` |
| Authentication | None (หรือดู Security ด้านล่าง) |
| Content Type | `JSON` |
| Body | `{"user_id": "{{ $json.userId }}", "text": "...", "modality": "conversation"}` |

### HTTP Request Node — POST /retrieve

| Field | ค่า |
|-------|-----|
| Method | `POST` |
| URL | `http://localhost:8001/retrieve` |
| Content Type | `JSON` |
| Body | `{"user_id": "{{ $json.userId }}", "text": "{{ $json.text }}"}` |

### HTTP Request Node — GET /categories

| Field | ค่า |
|-------|-----|
| Method | `GET` |
| URL | `http://localhost:8001/categories?user_id={{ $json.userId }}` |

---

## Security: API Key Authentication

เพื่อความปลอดภัย แนะนำให้เพิ่ม API key authentication:

### 1. เพิ่ม API Key ใน .env

```env
API_KEY=your-secret-api-key-here
```

### 2. ส่ง Header จาก N8N

ใน HTTP Request node → **Headers**:
```
X-API-Key: your-secret-api-key-here
```

### 3. ตั้งค่า Reverse Proxy (Production)

ใช้ Nginx หรือ Caddy เพื่อจำกัดการเข้าถึง API server จาก N8N เท่านั้น:

```nginx
location /memorize {
    allow 10.0.0.0/8;   # N8N server IP range
    deny all;
    proxy_pass http://localhost:8001;
}
```

---

## Deployment

### Local Development

```bash
cd examples/n8n
pip install -r requirements.txt memu
uvicorn memu-api-server:app --host 0.0.0.0 --port 8001 --reload
```

### Docker

```bash
# Build
docker build -t memu-api-n8n .

# Run
docker run -d \
  -p 8001:8001 \
  -e OPENAI_API_KEY=your_key \
  memu-api-n8n
```

### Docker Compose (N8N + memU API)

```yaml
services:
  memu-api:
    build: ./examples/n8n
    ports:
      - "8001:8001"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/memu
    depends_on:
      - db

  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=password
    volumes:
      - n8n_data:/home/node/.n8n

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: memu
      POSTGRES_PASSWORD: postgres
    volumes:
      - pg_data:/var/lib/postgresql/data

volumes:
  n8n_data:
  pg_data:
```

```bash
docker compose up -d
```

เข้า N8N ที่ `http://localhost:5678` และ import workflow จาก `examples/n8n/workflows/`

---

## ดูเพิ่มเติม

- [คู่มือการใช้งาน (README)](../../examples/n8n/README.md)
- [N8N Documentation](https://docs.n8n.io/)
- [LINE Messaging API](https://developers.line.biz/en/docs/messaging-api/)
- [memU GitHub](https://github.com/gittisak-go/memU)
