# N8N + memU Integration

> สร้าง **AI Agent ที่มีหน่วยความจำระยะยาว** ผ่าน N8N — ไม่ต้องเขียนโค้ด

---

## สารบัญ

- [ภาพรวมระบบ](#ภาพรวมระบบ)
- [ความต้องการเบื้องต้น](#ความต้องการเบื้องต้น)
- [ติดตั้งและรัน API Server](#ติดตั้งและรัน-api-server)
- [Import Workflow เข้า N8N](#import-workflow-เข้า-n8n)
- [ตั้งค่า Credentials](#ตั้งค่า-credentials)
- [API Endpoints](#api-endpoints)
- [Use Cases ภาษาไทย](#use-cases-ภาษาไทย)
- [การ Deploy](#การ-deploy)

---

## ภาพรวมระบบ

```
LINE User
    │
    │ ส่งข้อความ
    ▼
┌─────────────────────────────────────────────────────────┐
│                    N8N Workflow                          │
│                                                         │
│  LINE Webhook → Retrieve → OpenAI Chat → Memorize       │
│      Trigger     Memory       Node       Conversation   │
│                    │                        │           │
│                    ▼                        ▼           │
│              ┌──────────┐           ┌──────────┐       │
│              │  memU    │           │  memU    │       │
│              │  /retrieve│          │ /memorize│       │
│              └──────────┘           └──────────┘       │
│                    │                                    │
│                    └─→ Context → LINE Reply             │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
             ┌──────────────┐
             │  memU API    │   (FastAPI — runs locally or on server)
             │  Server      │
             └──────────────┘
                    │
                    ▼
             ┌──────────────┐
             │  memU Memory │   (SQLite / PostgreSQL / In-Memory)
             │  Store       │
             └──────────────┘
```

**จุดต่างจาก integration อื่น:**
- **ไม่ต้องเขียนโค้ด** — ใช้ N8N node ต่อกัน
- **รองรับ LINE Bot** ผ่าน N8N โดยตรง
- **Workflow พร้อม import** — ไม่ต้องสร้างเอง
- **เหมาะกับผู้ใช้ไทย** — ตอบสนองภาษาไทยได้ดี

---

## ความต้องการเบื้องต้น

| สิ่งที่ต้องมี | หมายเหตุ |
|---|---|
| Python 3.10+ | สำหรับรัน API Server |
| N8N (self-hosted หรือ cloud) | [n8n.io](https://n8n.io) |
| OpenAI API Key | [platform.openai.com](https://platform.openai.com) |
| LINE Messaging API (ถ้าใช้ LINE Bot) | [developers.line.biz](https://developers.line.biz) |
| memu package | ติดตั้งจาก repository หลัก |

---

## ติดตั้งและรัน API Server

### ขั้นตอนที่ 1 — ติดตั้ง dependencies

```bash
# จาก root ของ repository
pip install -e .

# ติดตั้ง dependencies เพิ่มเติมสำหรับ N8N integration
cd examples/n8n
pip install -r requirements.txt
```

### ขั้นตอนที่ 2 — ตั้งค่า environment variables

```bash
cp .env.example .env
```

แก้ไขไฟล์ `.env`:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBED_MODEL=text-embedding-3-small

# ถ้าต้องการบันทึกข้อมูลถาวร (ไม่เช่นนั้นข้อมูลจะหายเมื่อ restart)
DATABASE_URL=sqlite:///./memu_data.db

API_HOST=0.0.0.0
API_PORT=8000
```

### ขั้นตอนที่ 3 — รัน API Server

```bash
cd examples/n8n
uvicorn memu_api_server:app --host 0.0.0.0 --port 8000 --reload
```

ทดสอบว่า server ทำงาน:

```bash
curl http://localhost:8000/health
# → {"status":"ok","service":"memU API for N8N"}
```

ดู API documentation:

```
http://localhost:8000/docs
```

---

## Import Workflow เข้า N8N

### LINE Bot Workflow (`line_memu_bot.json`)

1. เปิด N8N → ไปที่ **Workflows**
2. คลิก **Import from file**
3. เลือกไฟล์ `workflows/line_memu_bot.json`
4. ตั้งค่า Environment Variables ใน N8N Settings:
   - `MEMU_API_URL` = `http://localhost:8000` (หรือ URL server ของคุณ)
   - `LINE_CHANNEL_ACCESS_TOKEN` = token จาก LINE Developer Console

### Daily Summary Workflow (`memory_dashboard.json`)

1. Import `workflows/memory_dashboard.json` เข้า N8N
2. ตั้งค่า Environment Variables:
   - `MEMU_API_URL` = URL ของ memU API Server
   - `LINE_CHANNEL_ACCESS_TOKEN` = LINE Channel Access Token
   - `DASHBOARD_USER_ID` = LINE User ID ที่ต้องการรับสรุปประจำวัน

---

## ตั้งค่า Credentials

### LINE Channel Access Token

1. ไปที่ [LINE Developer Console](https://developers.line.biz)
2. สร้าง **Messaging API channel** ใหม่
3. ไปที่ **Messaging API** tab → คัดลอก **Channel access token**
4. ตั้งค่า **Webhook URL** เป็น:
   ```
   https://<n8n-url>/webhook/line-webhook
   ```
5. เปิด **Use webhook** และปิด **Auto-reply messages**

### OpenAI API Key (ใน N8N)

1. ใน N8N → **Credentials** → **New** → เลือก **OpenAI**
2. ใส่ API key
3. กลับไปที่ workflow และเชื่อม OpenAI Chat node กับ credential นี้

---

## API Endpoints

### `POST /memorize` — บันทึกความจำ

```json
{
  "user_id": "Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "text": "ฉันชอบกินข้าวผัดกุ้ง และไม่ชอบผักชี",
  "modality": "conversation"
}
```

**Response:**
```json
{
  "success": true,
  "user_id": "Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "result": { "items": [...], "categories": [...] }
}
```

---

### `POST /retrieve` — ดึงความจำ

```json
{
  "user_id": "Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "text": "ฉันชอบกินอะไร?",
  "modality": "conversation"
}
```

**Response:**
```json
{
  "success": true,
  "user_id": "Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "memory_context": "- ชอบกินข้าวผัดกุ้ง\n- ไม่ชอบผักชี",
  "items": [...]
}
```

> **💡 เคล็ดลับ:** ใช้ `memory_context` ใส่ใน system prompt ของ OpenAI Chat node เพื่อให้ AI จำข้อมูลผู้ใช้

---

### `GET /categories?user_id=<id>` — ดูหมวดหมู่ความจำ

```bash
curl "http://localhost:8000/categories?user_id=Uxxxxxxxx"
```

**Response:**
```json
{
  "success": true,
  "user_id": "Uxxxxxxxx",
  "categories": [
    { "name": "preferences", "summary": "ชอบกินข้าวผัดกุ้ง..." },
    { "name": "personal_info", "summary": "ชื่อ สมชาย อายุ 30..." }
  ]
}
```

---

### `DELETE /memory` — ลบความจำ

```json
{
  "user_id": "Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

---

## Use Cases ภาษาไทย

### 🛍️ LINE Bot จำลูกค้า (Mini CRM)

ร้านค้าออนไลน์ที่ต้องการจำข้อมูลลูกค้าแต่ละคน:

```
ลูกค้า: "อยากได้เสื้อสีดำ ไซส์ M"
Bot (มีความจำ): "สวัสดีคุณมาลี! ครั้งที่แล้วคุณซื้อกางเกงสีกรมท่า 
                 เสื้อสีดำไซส์ M มีพร้อมส่งนะคะ ต้องการดูสีอื่นไหมคะ?"
```

**ตั้งค่า Workflow:**
- Retrieve memory ก่อนตอบ → ใส่ context ว่าลูกค้าซื้ออะไรมาก่อน
- Memorize หลังสนทนา → จำสินค้าที่ลูกค้าสนใจ

---

### ✅ To-Do Reminder ผ่าน LINE

Bot ที่จำ to-do list และ push notification ตอนเช้า:

```
ผู้ใช้: "เตือนฉันว่าต้องส่งรายงานวันศุกร์"
Bot: "จำแล้วครับ ฉันจะเตือนคุณในเช้าวันศุกร์"

[วันศุกร์ 08:00] Bot push: "📋 สรุปงานวันนี้:
- ส่งรายงานประจำเดือน
- ประชุม 14:00"
```

**ใช้ Workflow:** `memory_dashboard.json` (รัน 08:00 ทุกวัน)

---

### 💬 Customer Support Bot ที่จำ Context

Bot ช่วยเหลือลูกค้าที่จำประวัติปัญหาและวิธีแก้ไขที่เคยทำ:

```
ลูกค้า: "ปัญหาเดิมกลับมาอีกแล้ว"
Bot (มีความจำ): "คุณหมายถึงปัญหา connection timeout ที่เกิดเมื่อ 3 วันก่อนใช่ไหมครับ? 
                 ครั้งก่อนแก้ได้ด้วยการ restart service ลองทำดูก่อนนะครับ"
```

---

## การ Deploy

### รัน API Server บน Production

```bash
# ใช้ uvicorn โดยตรง
uvicorn memu_api_server:app --host 0.0.0.0 --port 8000 --workers 4

# หรือใช้ Docker (สร้าง Dockerfile เอง)
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-xxx \
  -e DATABASE_URL=sqlite:///./data/memu.db \
  -v ./data:/app/data \
  your-memu-api-image
```

### ตั้งค่า N8N Environment Variables

ใน N8N Settings → Variables:

| Variable | Value | หมายเหตุ |
|---|---|---|
| `MEMU_API_URL` | `http://memu-api:8000` | URL ของ API Server |
| `LINE_CHANNEL_ACCESS_TOKEN` | `xxxxxx` | จาก LINE Developer Console |
| `DASHBOARD_USER_ID` | `Uxxxxxxx` | LINE UID ผู้รับสรุปประจำวัน |

### ความปลอดภัย

- ใช้ HTTPS สำหรับ webhook URLs ใน production
- จำกัด access ของ memU API Server — ไม่ควร expose โดยตรงบน internet
- เก็บ API keys ใน environment variables ไม่ใส่ใน workflow โดยตรง
- ใช้ N8N Credentials system สำหรับ LINE และ OpenAI keys
