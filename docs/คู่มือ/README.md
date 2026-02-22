[🏠 หน้าหลัก](../../README.md) | [📚 สารบัญ](README.md)

---

# 📚 คู่มือการใช้งาน memU ภาษาไทย

ยินดีต้อนรับสู่คู่มือการใช้งาน memU ฉบับภาษาไทย เอกสารชุดนี้ออกแบบมาเพื่อช่วยให้คุณใช้งาน memU ได้อย่างมีประสิทธิภาพสูงสุด

---

## 📋 สารบัญ

| บท | ชื่อ | คำอธิบาย |
|----|-----|---------|
| 01 | [🚀 เริ่มต้นใช้งาน](01-เริ่มต้นใช้งาน.md) | การติดตั้ง, ตั้งค่า environment, และทดสอบครั้งแรก |
| 02 | [💡 แนวคิดหลัก](02-แนวคิดหลัก.md) | 3 ชั้นหน่วยความจำ, Proactive vs Reactive, Memory Lifecycle |
| 03 | [📖 API อ้างอิง](03-API-อ้างอิง.md) | `MemUService`, `memorize()`, `retrieve()`, การตั้งค่าทั้งหมด |
| 04 | [🔬 ตัวอย่างจริง](04-ตัวอย่างจริง.md) | 4 ตัวอย่างพร้อมโค้ดจาก repo จริง |
| 05 | [🐘 PostgreSQL + pgvector](05-การติดตั้ง-PostgreSQL.md) | ติดตั้ง PostgreSQL, Docker, ตั้งค่าฐานข้อมูล |
| 06 | [🔗 การผสานรวม](06-การผสานรวม.md) | LangGraph, OpenRouter, Custom LLM providers |

---

## 🗺️ แผนผังการเรียนรู้

```
เริ่มต้น
    │
    ▼
[บทที่ 1] เริ่มต้นใช้งาน
    ├── ติดตั้ง memU
    ├── ตั้งค่า API keys
    └── รันตัวอย่างแรก
         │
         ▼
[บทที่ 2] แนวคิดหลัก
    ├── ทำความเข้าใจ 3 ชั้นหน่วยความจำ
    ├── Proactive vs Reactive
    └── Memory Lifecycle
         │
         ▼
[บทที่ 3] API อ้างอิง
    ├── MemUService
    ├── memorize()
    └── retrieve()
         │
    ┌────┴────┐
    ▼         ▼
[บทที่ 4]  [บทที่ 5]
ตัวอย่างจริง  PostgreSQL
    │         │
    └────┬────┘
         ▼
[บทที่ 6] การผสานรวม
    ├── LangGraph
    ├── OpenRouter
    └── Custom LLM
```

---

## 🔗 ลิงก์ที่เกี่ยวข้อง

- 🏠 [README ภาษาไทย](../../readme/README_th.md)
- 🌐 [README หลัก (English)](../../README.md)
- 🧪 [ตัวอย่างโค้ด](../../examples/)
- 📂 [Source code](../../src/)
- 🐛 [รายงานปัญหา](https://github.com/NevaMind-AI/memU/issues)
- 💬 [Discord Community](https://discord.com/invite/hQZntfGsbJ)
