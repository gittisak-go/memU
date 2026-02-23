# memU

หน่วยความจำสำหรับเอเจนต์เชิงรุก 24/7 — เก็บความทรงจำระยะยาว ดัชนีเนื้อหา และเรียกคืนบริบทเมื่อจำเป็น เหมาะสำหรับการสร้าง chatbot, assistant และการผสานรวมกับ workflow อื่น ๆ

## ข้อมูลย่อ
- เก็บความทรงจำ (persisted memories)
- ค้นหาเชิงความหมาย (semantic search / embeddings) หากเปิดใช้งาน
- ตัวอย่างและเอกสารพร้อมใช้งานในโฟลเดอร์ `examples/` และ `docs/`

## วิธีติดตั้ง (สรุป)
```bash
git clone https://github.com/gittisak-go/memU.git
cd memU
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ตัวอย่างใช้งานเบื้องต้น (สมมติ)
```python
from memu import MemoryStore

store = MemoryStore()
store.save("พบลูกค้าชื่อสมชาย ชอบสีฟ้า")
results = store.search("ลูกค้าที่ชอบสีฟ้า")
for r in results:
    print(r.text, r.score)
```

## วิธีช่วยเหลือ / รายงานปัญหา
- เปิด Issue: https://github.com/gittisak-go/memU/issues
- ส่ง Pull Request สำหรับการปรับปรุง

## ใบอนุญาต
ดูไฟล์ `LICENSE` ในรีโป
