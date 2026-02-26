# N8N + memU Integration

เชื่อม **memU** กับ **N8N** workflow automation — สร้าง AI Agent ที่มีหน่วยความจำระยะยาวผ่าน N8N โดยไม่ต้องเขียนโค้ด รองรับ LINE Bot ด้วย workflow สำเร็จรูป

---

## สถาปัตยกรรม

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

N8N ทำหน้าที่เป็น no-code layer ประสานงานระหว่าง LINE, memU API server และ OpenAI โดยที่คุณไม่ต้องเขียนโค้ดเอง

---

## ไฟล์ในโฟลเดอร์นี้

```
examples/n8n/
├── memu-api-server.py          ← FastAPI server ที่ N8N เรียกได้
├── requirements.txt            ← Python dependencies
├── .env.example                ← ตัวอย่าง environment variables
└── workflows/
    ├── line-memu-bot.json      ← N8N workflow: LINE Bot + memU
    └── memory-dashboard.json  ← N8N workflow: สรุปความจำประจำวัน
```

---

## ขั้นตอนติดตั้ง

### 1. ติดตั้ง API Server

```bash
cd examples/n8n

# คัดลอก .env และแก้ไข API key
cp .env.example .env
# แก้ไข OPENAI_API_KEY ใน .env

# ติดตั้ง dependencies
pip install -r requirements.txt

# รัน API server
uvicorn memu-api-server:app --host 0.0.0.0 --port 8001
```

> **หมายเหตุ:** ต้องติดตั้ง `memu` package ก่อน:
> ```bash
> pip install memu
> ```

### 2. ทดสอบ API Server

```bash
# Health check
curl http://localhost:8001/health

# บันทึกความจำ
curl -X POST http://localhost:8001/memorize \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "text": "ฉันชอบกาแฟอเมริกาโน่", "modality": "conversation"}'

# ดึงความจำ
curl -X POST http://localhost:8001/retrieve \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "text": "ฉันชอบดื่มอะไร"}'

# ดูหมวดหมู่ความจำ
curl "http://localhost:8001/categories?user_id=test_user"

# ลบความจำ
curl -X DELETE http://localhost:8001/memory \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user"}'
```

---

## Import Workflow เข้า N8N

### LINE Bot Workflow

1. เปิด N8N → **Workflows** → **Import from File**
2. เลือกไฟล์ `workflows/line-memu-bot.json`
3. ตั้งค่า Credentials ตามหัวข้อด้านล่าง
4. แก้ไข URL ของ memU API server ให้ตรงกับ environment ของคุณ
5. **Activate** workflow

### Memory Dashboard Workflow

1. Import `workflows/memory-dashboard.json`
2. แก้ไข `YOUR_LINE_USER_ID` ใน node **LINE Push สรุปความจำ** ให้เป็น LINE User ID ของคุณ
3. ตั้งค่า LINE credential
4. **Activate** workflow

---

## ตั้งค่า Credentials ใน N8N

### LINE Messaging API

1. ไป **Settings** → **Credentials** → **New Credential**
2. เลือก **HTTP Header Auth**
3. ตั้งชื่อ: `LINE API`
4. Header Name: `Authorization`
5. Header Value: `Bearer YOUR_LINE_CHANNEL_ACCESS_TOKEN`

### OpenAI

1. สร้าง Credential ใหม่ชื่อ **HTTP Header Auth**
2. Header Name: `Authorization`
3. Header Value: `Bearer YOUR_OPENAI_API_KEY`

### ใช้ Credentials ใน Node

ใน HTTP Request node ที่เรียก LINE หรือ OpenAI:
- **Authentication** → `Generic Credential Type`
- **Generic Auth Type** → `HTTP Header Auth`
- **Credential** → เลือก credential ที่สร้างไว้

---

## ตั้งค่า HTTP Request Node

Node ที่เรียก memU API server ต้องตั้งค่าดังนี้:

| Field | ค่า |
|-------|-----|
| Method | POST (หรือ GET, DELETE ตาม endpoint) |
| URL | `http://localhost:8001/memorize` |
| Content Type | JSON |
| Body | `{"user_id": "...", "text": "...", "modality": "conversation"}` |

หาก API server อยู่บน server อื่น ให้เปลี่ยน `localhost:8001` เป็น IP/hostname จริง

---

## LINE Webhook Setup

1. เปิด [LINE Developers Console](https://developers.line.biz/)
2. เลือก Channel → **Messaging API**
3. **Webhook URL**: `https://your-n8n-domain.com/webhook/line-webhook`
4. เปิด **Use webhook**
5. ปิด **Auto-reply messages** (ให้ N8N ตอบเอง)

---

## ตัวอย่าง Use Cases

### 1. LINE Bot จำชื่อลูกค้า

ลูกค้าพิมพ์ว่า "สวัสดีครับ ผมชื่อสมชาย" → Bot บันทึกชื่อไว้ใน memU
ครั้งต่อไปลูกค้าพิมพ์ว่า "ช่วยแนะนำสินค้าหน่อย" → Bot เรียกความจำและตอบว่า "สวัสดีครับคุณสมชาย..."

**วิธีทำ:** ใช้ workflow `line-memu-bot.json` ตามปกติ memU จะจำข้อมูลลูกค้าโดยอัตโนมัติ

### 2. บันทึก To-Do จาก LINE

ผู้ใช้พิมพ์ "ต้องโทรหาหมอพรุ่งนี้ตอนบ่าย 2" → memU จำ to-do ไว้
เมื่อถามว่า "วันนี้ต้องทำอะไรบ้าง" → Bot ดึงความจำและแจ้งรายการงาน

**วิธีทำ:** ใช้ workflow `line-memu-bot.json` ร่วมกับ `memory-dashboard.json` สำหรับแจ้งเตือนประจำวัน

### 3. CRM เบื้องต้นสำหรับร้านค้า

เจ้าของร้านบันทึกข้อมูลลูกค้าผ่าน LINE: "คุณมาลี สั่งของทุกเดือน ชอบสีชมพู"
เมื่อลูกค้ากลับมา Bot จำประวัติและแนะนำสินค้าที่เหมาะสม

**วิธีทำ:** แต่ละลูกค้าใช้ `user_id` ของ LINE ที่ไม่ซ้ำกัน memU แยกความจำตาม user_id โดยอัตโนมัติ

---

## API Endpoints Reference

| Method | Path | คำอธิบาย |
|--------|------|-----------|
| `GET` | `/health` | ตรวจสอบสถานะ server |
| `POST` | `/memorize` | บันทึกข้อความลงหน่วยความจำ |
| `POST` | `/retrieve` | ดึงความจำที่เกี่ยวข้อง |
| `GET` | `/categories?user_id=xxx` | ดูหมวดหมู่ความจำ |
| `DELETE` | `/memory` | ลบความจำทั้งหมดของ user |

### Request Body (POST /memorize, POST /retrieve)

```json
{
  "user_id": "line_uid_xxx",
  "text": "ข้อความ",
  "modality": "conversation"
}
```

### Response (POST /retrieve)

```json
{
  "status": "ok",
  "user_id": "line_uid_xxx",
  "summary": "สรุปความจำที่เกี่ยวข้อง...",
  "memories": [...],
  "count": 3
}
```

---

## การใช้ PostgreSQL แทน In-Memory Storage

เพิ่มใน `.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/memu
```

API server จะใช้ PostgreSQL โดยอัตโนมัติเมื่อตั้งค่า `DATABASE_URL`

---

## Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt memu
COPY memu-api-server.py .
COPY .env .
EXPOSE 8001
CMD ["uvicorn", "memu-api-server:app", "--host", "0.0.0.0", "--port", "8001"]
```

```bash
docker build -t memu-api .
docker run -d -p 8001:8001 --env-file .env memu-api
```
