# LINE Bot Integration

เอกสารอ้างอิงฉบับสมบูรณ์สำหรับการ integrate LINE Messaging API เข้ากับ memU

---

## Architecture

```
LINE User
   │
   ▼
LINE Platform (Messaging API)
   │  webhook POST /callback
   ▼
FastAPI App (line_bot.py)
   │
   ├─► memU.memorize()  ← บันทึกข้อความผู้ใช้
   │
   ├─► memU.retrieve()  ← ดึงความจำที่เกี่ยวข้อง
   │
   ├─► OpenAI (สร้างคำตอบ + context จาก memU)
   │
   └─► LINE Reply API  ← ส่งคำตอบกลับ
```

---

## Flow การทำงานทีละขั้น

1. ผู้ใช้ส่งข้อความใน LINE
2. LINE Platform ส่ง `POST /callback` พร้อม signature มาที่ Bot server
3. Bot ตรวจสอบ **X-Line-Signature** header (HMAC-SHA256 จาก Channel Secret)
4. ดึง `user_id` ของผู้ใช้จาก event
5. เรียก `memU.memorize()` เพื่อบันทึกข้อความของผู้ใช้
6. เรียก `memU.retrieve()` เพื่อดึงความจำที่เกี่ยวข้องกับข้อความปัจจุบัน
7. ส่งความจำเป็น context ให้ OpenAI สร้างคำตอบ
8. เรียก LINE Reply API ส่งคำตอบกลับไปยังผู้ใช้

---

## การตั้งค่า memU สำหรับ LINE (User Scoping)

memU ใช้ `user_id` จาก LINE เป็น key แยกหน่วยความจำต่อคน:

```python
from memu.app.service import MemoryService

service = MemoryService(
    llm_profiles={
        "default": {
            "api_key": OPENAI_API_KEY,
            "chat_model": "gpt-4o-mini",
        },
    },
)

# บันทึกความจำของผู้ใช้คนนั้น
await service.memorize(
    resource_url=message_text,
    modality="conversation",
    user={"user_id": line_user_id},
)

# ดึงความจำของผู้ใช้คนนั้น
result = await service.retrieve(
    queries=[{"role": "user", "content": {"text": message_text}}],
    where={"user_id": line_user_id},
)
```

ผู้ใช้แต่ละคนจะมีพื้นที่ความจำแยกอิสระจากกัน

---

## Security: ตรวจสอบ Signature จาก LINE

LINE Platform ส่ง signature ใน header `X-Line-Signature` ทุก request  
Bot **ต้องตรวจสอบ** signature ก่อนประมวลผล เพื่อป้องกัน request ปลอม

```python
from linebot.v3 import WebhookParser
from linebot.v3.exceptions import InvalidSignatureError

parser = WebhookParser(LINE_CHANNEL_SECRET)

@app.post("/callback")
async def callback(request: Request):
    signature = request.headers.get("X-Line-Signature", "")
    body = await request.body()

    try:
        events = parser.parse(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    # ...
```

LINE SDK (`line-bot-sdk>=3.0.0`) ทำการตรวจสอบ HMAC-SHA256 ให้อัตโนมัติ

---

## Rate Limiting และ Best Practices

| หัวข้อ | คำแนะนำ |
|--------|---------|
| Reply Token | ใช้ได้ครั้งเดียวและหมดอายุใน 30 วินาที |
| Webhook Timeout | LINE คาด response ภายใน **1 วินาที** — ประมวลผล async หนักหลัง reply |
| Rate Limit | LINE Free tier: 500 messages/เดือน |
| Error Handling | Catch exception ทุก call ไม่ให้ Bot crash |
| Logging | Log `user_id` และ message สำหรับ debug |
| Secrets | เก็บ credentials ใน environment variables เสมอ ห้าม hardcode |

---

## ตัวอย่าง Use Cases

### 1. ผู้ช่วยส่วนตัว
Bot จำนิสัย ความชอบ ตารางนัดหมาย และตอบคำถามได้แบบรู้จักผู้ใช้จริง

```
ผู้ใช้: ฉันแพ้กุ้ง
Bot:    บันทึกแล้วครับ จะไม่แนะนำเมนูที่มีกุ้งให้คุณอีก

ผู้ใช้: วันนี้กินอะไรดี?
Bot:    แนะนำข้าวผัดไก่หรือผัดซีอิ๊วหมูครับ (หลีกเลี่ยงกุ้งตามที่คุณแจ้งไว้)
```

### 2. บันทึกความจำ / Note-taking
```
ผู้ใช้: จด: ประชุมพรุ่งนี้ 10 โมง
Bot:    บันทึกแล้วครับ — ประชุมพรุ่งนี้ 10:00

ผู้ใช้: พรุ่งนี้มีอะไรบ้าง?
Bot:    พรุ่งนี้มีประชุม 10:00 ครับ
```

### 3. Chatbot ร้านค้า
Bot จำประวัติการสั่งซื้อ ความชอบ และแนะนำสินค้าส่วนตัว:

```
ผู้ใช้: อยากสั่งกาแฟแบบเดิม
Bot:    อเมริกาโน่ร้อนไม่น้ำตาล ขนาด M เหมือนครั้งที่แล้วใช่ไหมครับ?
```

---

## สิ่งที่เกี่ยวข้อง

- [examples/line_bot/](../../examples/line_bot/) — โค้ด Bot และคู่มือ
- [LINE Messaging API Docs](https://developers.line.biz/en/docs/messaging-api/)
- [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)
