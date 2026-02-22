# LINE Bot Integration สำหรับ memU

ผสาน **LINE Messaging API** เข้ากับ memU เพื่อให้ผู้ใช้ LINE คุยกับ AI Agent ที่มีหน่วยความจำระยะยาวได้ทันที

---

## LINE Bot คืออะไร และทำไมต้อง integrate กับ memU?

**LINE Bot** คือบัญชี LINE ที่ควบคุมโดยโปรแกรม รับ-ส่งข้อความผ่าน LINE Messaging API  
เมื่อเชื่อมกับ **memU** Bot จะสามารถ:

- **จดจำ** บทสนทนาก่อนหน้าของแต่ละคนแยกกัน
- **ดึงความจำ** ที่เกี่ยวข้องมาใช้ตอบทุกครั้ง
- ทำงานเหมือนผู้ช่วยส่วนตัวที่รู้จักคุณจริง ๆ

---

## สิ่งที่ต้องมีก่อน

| รายการ | รายละเอียด |
|--------|-----------|
| Python 3.11+ | ติดตั้งแล้ว |
| LINE Developers Account | [สมัครฟรี](https://developers.line.biz/) |
| OpenAI API Key | [console.openai.com](https://platform.openai.com/) |
| ngrok (ทดสอบ local) | [ngrok.com](https://ngrok.com/) |

---

## ขั้นตอนสร้าง LINE Bot บน LINE Developers Console

### 1. สร้าง Provider

1. ไปที่ [LINE Developers Console](https://developers.line.biz/console/)
2. คลิก **Create a new provider** → ตั้งชื่อ (เช่น `My memU Bot`)
3. คลิก **Create**

### 2. สร้าง Messaging API Channel

1. ใน Provider ที่สร้าง คลิก **Create a new channel**
2. เลือก **Messaging API**
3. กรอกข้อมูล:
   - **Channel name**: ชื่อ Bot ของคุณ
   - **Channel description**: คำอธิบาย
   - **Category / Subcategory**: เลือกตามต้องการ
4. คลิก **Create**

### 3. เก็บ Credentials

ใน tab **Basic settings**:
- คัดลอก **Channel secret** → ใช้เป็น `LINE_CHANNEL_SECRET`

ใน tab **Messaging API**:
- เลื่อนลงถึง **Channel access token** → คลิก **Issue** → คัดลอก → ใช้เป็น `LINE_CHANNEL_ACCESS_TOKEN`

### 4. ปิด Auto-reply

ใน tab **Messaging API** → **LINE Official Account features**:
- **Auto-reply messages** → คลิก **Edit** → ปิด
- **Greeting messages** → ปิด (ตามต้องการ)

---

## Environment Variables

คัดลอกไฟล์ตัวอย่าง แล้วใส่ค่าจริง:

```bash
cp .env.example .env
```

แก้ไข `.env`:

```env
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
LINE_CHANNEL_SECRET=your_line_channel_secret
OPENAI_API_KEY=your_openai_api_key
```

---

## ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
pip install memu
```

หรือถ้าใช้ `uv`:

```bash
uv pip install -r requirements.txt memu
```

---

## รันบนเครื่อง (Local) + Expose ด้วย ngrok

### 1. รัน Bot

```bash
uvicorn line_bot:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Expose ด้วย ngrok

เปิด terminal ใหม่:

```bash
ngrok http 8000
```

ngrok จะแสดง URL เช่น `https://xxxx-xx-xx-xx-xx.ngrok-free.app`

### 3. ตั้ง Webhook URL

ใน LINE Developers Console → **Messaging API** tab:
- **Webhook URL**: `https://xxxx-xx-xx-xx-xx.ngrok-free.app/callback`
- คลิก **Verify** → ต้องขึ้น Success
- เปิด **Use webhook**

---

## Deploy บน Cloud

### Railway

```bash
# ติดตั้ง Railway CLI
npm install -g @railway/cli
railway login
railway init
railway up
```

เพิ่ม Environment Variables ใน Railway Dashboard แล้วตั้ง Webhook URL เป็น URL ของ Railway

### Render

1. Push โค้ดไป GitHub
2. ไปที่ [render.com](https://render.com) → **New Web Service**
3. เชื่อม Repository → Build Command: `pip install -r requirements.txt memu`
4. Start Command: `uvicorn line_bot:app --host 0.0.0.0 --port $PORT`
5. เพิ่ม Environment Variables → Deploy
6. ตั้ง Webhook URL เป็น URL ของ Render

### Fly.io

```bash
fly launch
fly secrets set LINE_CHANNEL_ACCESS_TOKEN=xxx LINE_CHANNEL_SECRET=xxx OPENAI_API_KEY=xxx
fly deploy
```

---

## ตัวอย่างการสนทนาที่ Bot จดจำได้

```
ผู้ใช้: สวัสดี ฉันชื่อสมชาย ชอบกินข้าวผัดกะเพรา
Bot:    สวัสดีครับ สมชาย! บันทึกความชอบของคุณไว้แล้วครับ

--- (วันถัดไป) ---

ผู้ใช้: วันนี้จะกินอะไรดี?
Bot:    คุณสมชายชอบกินข้าวผัดกะเพราครับ วันนี้ลองกินที่ร้านโปรดดูไหมครับ?

--- (อีก 3 วันถัดมา) ---

ผู้ใช้: ช่วยแนะนำหนังดู
Bot:    แนะนำแนวไหนดีครับ มีแนวที่ชอบเป็นพิเศษไหม? 
        (Bot จำได้ว่าคุณเป็นใคร แต่ยังไม่รู้ว่าชอบหนังแนวไหน)
```

---

## โครงสร้างไฟล์

```
examples/line_bot/
├── line_bot.py        # FastAPI webhook handler
├── requirements.txt   # Python dependencies
├── .env.example       # ตัวอย่าง environment variables
└── README.md          # คู่มือนี้
```
