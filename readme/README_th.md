![MemU Banner](../assets/banner.png)

<div align="center">

# memU

### ระบบหน่วยความจำเชิงรุก 24/7 สำหรับ AI Agents

[![PyPI version](https://badge.fury.io/py/memu-py.svg)](https://badge.fury.io/py/memu-py)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Discord](https://img.shields.io/badge/Discord-Join%20Chat-5865F2?logo=discord&logoColor=white)](https://discord.gg/memu)
[![Twitter](https://img.shields.io/badge/Twitter-Follow-1DA1F2?logo=x&logoColor=white)](https://x.com/memU_ai)

<a href="https://trendshift.io/repositories/17374" target="_blank"><img src="https://trendshift.io/api/badge/repositories/17374" alt="NevaMind-AI%2FmemU | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

**[English](README_en.md) | [中文](README_zh.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Español](README_es.md) | [Français](README_fr.md) | [ภาษาไทย](README_th.md)**

</div>

---

memU คือ framework ด้านหน่วยความจำที่ออกแบบมาสำหรับ **agent ที่ทำงานเชิงรุกตลอด 24/7**
รองรับการทำงานระยะยาวและช่วย**ลดต้นทุน LLM token** สำหรับการดูแล agent ให้ออนไลน์อยู่เสมอ ทำให้ agent ที่พัฒนาตัวเองได้อย่างต่อเนื่องกลายเป็นเรื่องที่ทำได้จริงในระบบ production
memU **จับและทำความเข้าใจเจตนาของผู้ใช้อย่างต่อเนื่อง** แม้ไม่มีคำสั่ง agent ก็สามารถบอกได้ว่าคุณกำลังจะทำอะไรและลงมือทำแทนได้เอง

---

## 🤖 [OpenClaw (Moltbot, Clawdbot) Alternative](https://memu.bot)

<img width="100%" src="https://github.com/NevaMind-AI/memU/blob/main/assets/memUbot.png" />

- **ดาวน์โหลดแล้วใช้งานได้เลย** ไม่ซับซ้อน
- สร้างหน่วยความจำระยะยาวเพื่อ **เข้าใจเจตนาผู้ใช้** และทำงานเชิงรุก
- **ลดต้นทุน LLM token** ด้วย context ที่เล็กลง

ลองใช้เลย: [memU bot](https://memu.bot)

---

## 🗃️ หน่วยความจำเหมือน File System, File System เหมือนหน่วยความจำ

memU จัดการ **หน่วยความจำเหมือน file system** — มีโครงสร้าง, ลำดับชั้น, และเข้าถึงได้ทันที

| File System | หน่วยความจำ memU |
|-------------|-----------------|
| 📁 Folders | 🏷️ Categories (หัวข้อที่จัดระเบียบอัตโนมัติ) |
| 📄 Files | 🧠 Memory Items (ข้อเท็จจริง, ความชอบ, ทักษะที่สกัดออกมา) |
| 🔗 Symlinks | 🔄 Cross-references (ความทรงจำที่เกี่ยวข้องเชื่อมถึงกัน) |
| 📂 Mount points | 📥 Resources (บทสนทนา, เอกสาร, ภาพ) |

**ทำไมถึงสำคัญ:**
- **นำทางในหน่วยความจำ** เหมือนเรียกดู directory — เจาะลึกจาก category ใหญ่ไปถึงข้อเท็จจริงเฉพาะเรื่อง
- **เพิ่มความรู้ใหม่ได้ทันที** — บทสนทนาและเอกสารกลายเป็นหน่วยความจำที่ค้นหาได้
- **เชื่อมโยงทุกอย่าง** — ความทรงจำอ้างอิงถึงกัน สร้าง knowledge graph ที่เชื่อมต่อกัน
- **ถาวรและพกพาได้** — export, backup, และย้ายหน่วยความจำเหมือนไฟล์

```
memory/
├── preferences/
│   ├── communication_style.md
│   └── topic_interests.md
├── relationships/
│   ├── contacts/
│   └── interaction_history/
├── knowledge/
│   ├── domain_expertise/
│   └── learned_skills/
└── context/
    ├── recent_conversations/
    └── pending_tasks/
```

เหมือนที่ file system เปลี่ยน raw bytes เป็นข้อมูลที่มีระเบียบ memU แปลง interaction ดิบๆ ให้เป็น **ข้อมูลอัจฉริยะที่มีโครงสร้าง ค้นหาได้ และทำงานเชิงรุก**

---

## ⭐️ ให้ดาวโปรเจกต์

<img width="100%" src="https://github.com/NevaMind-AI/memU/blob/main/assets/star.gif" />
ถ้าคุณพบว่า memU มีประโยชน์หรือน่าสนใจ GitHub Star ⭐️ จะเป็นสิ่งที่เราขอบคุณมาก

---

## ✨ คุณสมบัติหลัก

| ความสามารถ | คำอธิบาย |
|-----------|---------|
| 🤖 **Agent เชิงรุก 24/7** | Memory agent ที่ทำงานอย่างต่อเนื่องในพื้นหลัง — ไม่เคยหลับ ไม่เคยลืม |
| 🎯 **จับเจตนาผู้ใช้** | เข้าใจและจดจำเป้าหมาย ความชอบ และ context ของผู้ใช้ข้ามเซสชันโดยอัตโนมัติ |
| 💰 **ประหยัดต้นทุน** | ลดต้นทุน token ระยะยาวด้วยการ cache insights และหลีกเลี่ยงการเรียก LLM ซ้ำ |

---

## 🔄 การทำงานของ Proactive Memory

```bash
cd examples/proactive
python proactive.py
```

---

### วงจรชีวิต Proactive Memory
```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                         USER QUERY                                               │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
                 │                                                           │
                 ▼                                                           ▼
┌────────────────────────────────────────┐         ┌────────────────────────────────────────────────┐
│         🤖 MAIN AGENT                  │         │              🧠 MEMU BOT                       │
│                                        │         │                                                │
│  จัดการ query และรันงาน               │  ◄───►  │  ติดตาม, จดจำ และ proactive intelligence      │
├────────────────────────────────────────┤         ├────────────────────────────────────────────────┤
│                                        │         │                                                │
│  ┌──────────────────────────────────┐  │         │  ┌──────────────────────────────────────────┐  │
│  │  1. รับ INPUT จากผู้ใช้          │  │         │  │  1. ติดตาม INPUT/OUTPUT                  │  │
│  │     วิเคราะห์ query ทำความเข้าใจ │  │   ───►  │  │     สังเกต agent interactions            │  │
│  │     context และเจตนา             │  │         │  │     ติดตาม conversation flow             │  │
│  └──────────────────────────────────┘  │         │  └──────────────────────────────────────────┘  │
│                 │                      │         │                    │                           │
│                 ▼                      │         │                    ▼                           │
│  ┌──────────────────────────────────┐  │         │  ┌──────────────────────────────────────────┐  │
│  │  2. วางแผนและรันงาน              │  │         │  │  2. MEMORIZE & EXTRACT                   │  │
│  │     แบ่งงาน เรียกใช้ tools       │  │   ◄───  │  │     เก็บ insights, facts, ความชอบ        │  │
│  │     สร้างคำตอบ                   │  │  inject │  │     สกัดทักษะและความรู้                  │  │
│  │                                  │  │  memory │  │     อัปเดต user profile                  │  │
│  └──────────────────────────────────┘  │         │  └──────────────────────────────────────────┘  │
│                 │                      │         │                    │                           │
│                 ▼                      │         │                    ▼                           │
│  ┌──────────────────────────────────┐  │         │  ┌──────────────────────────────────────────┐  │
│  │  3. ตอบผู้ใช้                    │  │         │  │  3. คาดเดาเจตนาผู้ใช้                   │  │
│  │     ส่งคำตอบ/ผลลัพธ์             │  │   ───►  │  │     คาดการณ์ขั้นตอนถัดไป               │  │
│  │     สานต่อบทสนทนา               │  │         │  │     ระบุความต้องการที่จะมาถึง            │  │
│  └──────────────────────────────────┘  │         │  └──────────────────────────────────────────┘  │
│                 │                      │         │                    │                           │
│                 ▼                      │         │                    ▼                           │
│  ┌──────────────────────────────────┐  │         │  ┌──────────────────────────────────────────┐  │
│  │  4. วนซ้ำ                        │  │         │  │  4. รัน PROACTIVE TASKS                  │  │
│  │     รอ input ถัดไปจากผู้ใช้      │  │   ◄───  │  │     ดึง context ที่เกี่ยวข้องล่วงหน้า  │  │
│  │     หรือคำแนะนำเชิงรุก          │  │  suggest│  │     เตรียม recommendations               │  │
│  └──────────────────────────────────┘  │         │  │     อัปเดต todolist อัตโนมัติ           │  │
│                                        │         │  └──────────────────────────────────────────┘  │
└────────────────────────────────────────┘         └────────────────────────────────────────────────┘
                 │                                                           │
                 └───────────────────────────┬───────────────────────────────┘
                                             ▼
                              ┌──────────────────────────────┐
                              │     CONTINUOUS SYNC LOOP     │
                              │  Agent ◄──► MemU Bot ◄──► DB │
                              └──────────────────────────────┘
```

---

## 🎯 กรณีการใช้งานเชิงรุก

### 1. **แนะนำข้อมูล**
*Agent ติดตามความสนใจและนำเสนอเนื้อหาที่เกี่ยวข้องเชิงรุก*
```python
# ผู้ใช้กำลังค้นคว้าหัวข้อ AI
MemU tracks: reading history, saved articles, search queries

# เมื่อมีเนื้อหาใหม่:
Agent: "ฉันพบบทความใหม่ 3 ชิ้นเกี่ยวกับ RAG optimization ที่ตรงกับ
        การวิจัยของคุณเกี่ยวกับ retrieval systems ล่าสุด ผู้เขียนคนหนึ่ง
        (Dr. Chen) ที่คุณเคยอ้างอิงเพิ่งเผยแพร่เมื่อวานนี้"
```

### 2. **จัดการอีเมล**
*Agent เรียนรู้รูปแบบการสื่อสารและจัดการงานปกติ*
```python
# MemU สังเกต patterns ของอีเมลตามเวลา:
- template คำตอบสำหรับสถานการณ์ทั่วไป
- ผู้ติดต่อสำคัญและคำสำคัญเร่งด่วน
- ความชอบด้านตารางเวลาและความพร้อม

# ช่วยเหลือด้านอีเมลเชิงรุก:
Agent: "มีอีเมลใหม่ 12 ฉบับ ฉันร่างคำตอบสำหรับ 3 คำขอทั่วไปแล้ว
        และทำเครื่องหมาย 2 รายการเร่งด่วนจากผู้ติดต่อสำคัญของคุณ"
```

### 3. **ติดตามการซื้อขายและการเงิน**
*Agent ติดตาม context ของตลาดและพฤติกรรมการลงทุนของผู้ใช้*
```python
# MemU เรียนรู้ความชอบด้านการซื้อขาย:
- ความเสี่ยงที่ยอมรับได้จากการตัดสินใจในอดีต
- sector และ asset class ที่ชอบ

# แจ้งเตือนเชิงรุก:
Agent: "NVDA ลดลง 5% ใน after-hours trading จากพฤติกรรมของคุณในอดีต
        คุณมักซื้อ tech เมื่อลดลงมากกว่า 3% การจัดสรรปัจจุบันของคุณ
        อนุญาตให้เพิ่มความเสี่ยง $2,000 ได้"
```

---

## 🗂️ สถาปัตยกรรมหน่วยความจำแบบลำดับชั้น

ระบบ 3 ชั้นของ memU รองรับทั้ง **reactive queries** และ **proactive context loading**:

<img width="100%" alt="structure" src="../assets/structure.png" />

| ชั้น | Reactive Use | Proactive Use |
|-----|--------------|---------------|
| **Resource** | เข้าถึงข้อมูลต้นฉบับโดยตรง | ติดตามพื้นหลังสำหรับ patterns ใหม่ |
| **Item** | ดึงข้อเท็จจริงเฉพาะเจาะจง | สกัดแบบ real-time จาก interactions ที่กำลังดำเนินอยู่ |
| **Category** | ภาพรวมระดับสรุป | รวม context อัตโนมัติเพื่อการคาดการณ์ |

---

## 🚀 เริ่มต้นใช้งานอย่างรวดเร็ว

### ตัวเลือก 1: Cloud Version

ลอง proactive memory ได้ทันที:

👉 **[memu.so](https://memu.so)** — บริการโฮสต์พร้อม continuous learning 24/7

#### Cloud API (v3)

| Base URL | `https://api.memu.so` |
|----------|----------------------|
| Auth | `Authorization: Bearer YOUR_API_KEY` |

| Method | Endpoint | คำอธิบาย |
|--------|----------|---------|
| `POST` | `/api/v3/memory/memorize` | ลงทะเบียน continuous learning task |
| `GET` | `/api/v3/memory/memorize/status/{task_id}` | ตรวจสอบสถานะการประมวลผล |
| `POST` | `/api/v3/memory/categories` | แสดง categories ที่สร้างอัตโนมัติ |
| `POST` | `/api/v3/memory/retrieve` | ค้นหาหน่วยความจำ |

---

### ตัวเลือก 2: Self-Hosted

#### การติดตั้ง
```bash
pip install -e .
```

> **ข้อกำหนด**: Python 3.13+ และ OpenAI API key

**ทดสอบ Continuous Learning** (in-memory):
```bash
export OPENAI_API_KEY=your_api_key
cd tests
python test_inmemory.py
```

**ทดสอบกับ Persistent Storage** (PostgreSQL):
```bash
# เริ่ม PostgreSQL พร้อม pgvector
docker run -d \
  --name memu-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=memu \
  -p 5432:5432 \
  pgvector/pgvector:pg16

export OPENAI_API_KEY=your_api_key
cd tests
python test_postgres.py
```

---

### Custom LLM และ Embedding Providers

memU รองรับ LLM และ embedding providers ที่กำหนดเองนอกจาก OpenAI ตั้งค่าผ่าน `llm_profiles`:
```python
from memu import MemUService

service = MemUService(
    llm_profiles={
        # Profile หลักสำหรับ LLM operations
        "default": {
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "api_key": "your_api_key",
            "chat_model": "qwen3-max",
            "client_backend": "sdk"  # "sdk" หรือ "http"
        },
        # Profile แยกสำหรับ embeddings
        "embedding": {
            "base_url": "https://api.voyageai.com/v1",
            "api_key": "your_voyage_api_key",
            "embed_model": "voyage-3.5-lite"
        }
    },
    # ... การตั้งค่าอื่นๆ
)
```

---

### OpenRouter Integration

memU รองรับ [OpenRouter](https://openrouter.ai) เป็น model provider ให้คุณเข้าถึง LLM provider หลายตัวผ่าน API เดียว

```python
from memu.app import MemoryService

service = MemoryService(
    llm_profiles={
        "default": {
            "provider": "openrouter",
            "client_backend": "httpx",
            "base_url": "https://openrouter.ai",
            "api_key": "your_openrouter_api_key",
            "chat_model": "anthropic/claude-3.5-sonnet",
            "embed_model": "openai/text-embedding-3-small",
        },
    },
    database_config={
        "metadata_store": {"provider": "inmemory"},
    },
)
```

---

## 📖 Core APIs

### `memorize()` — Continuous Learning Pipeline

ประมวลผล input แบบ real-time และอัปเดตหน่วยความจำทันที:

<img width="100%" alt="memorize" src="../assets/memorize.png" />

```python
result = await service.memorize(
    resource_url="path/to/file.json",  # เส้นทางไฟล์หรือ URL
    modality="conversation",            # conversation | document | image | video | audio
    user={"user_id": "123"}             # Optional: กำหนดขอบเขตผู้ใช้
)

# คืนค่าทันทีพร้อมหน่วยความจำที่สกัดออกมา:
{
    "resource": {...},      # metadata ของ resource ที่จัดเก็บ
    "items": [...],         # memory items ที่สกัดแล้ว (พร้อมใช้งานทันที)
    "categories": [...]     # โครงสร้าง category ที่อัปเดตอัตโนมัติ
}
```

### `retrieve()` — Dual-Mode Intelligence

<img width="100%" alt="retrieve" src="../assets/retrieve.png" />

#### RAG-based Retrieval (`method="rag"`)
ดึง **proactive context** รวดเร็วด้วย embeddings:
- ✅ **Context ทันที**: ดึงหน่วยความจำใน sub-second
- ✅ **ติดตามพื้นหลัง**: รันต่อเนื่องโดยไม่มีต้นทุน LLM

#### LLM-based Retrieval (`method="llm"`)
**การให้เหตุผลเชิงคาดการณ์** ที่ลึกสำหรับ context ซับซ้อน:
- ✅ **คาดเดาเจตนา**: LLM อนุมานสิ่งที่ผู้ใช้ต้องการก่อนถาม
- ✅ **วิวัฒนาการ query**: ปรับแต่งการค้นหาอัตโนมัติ

#### การเปรียบเทียบ

| ด้าน | RAG (Fast Context) | LLM (Deep Reasoning) |
|-----|-------------------|---------------------|
| **ความเร็ว** | ⚡ มิลลิวินาที | 🐢 วินาที |
| **ต้นทุน** | 💰 Embedding เท่านั้น | 💰💰 LLM inference |
| **Proactive use** | ติดตามต่อเนื่อง | โหลด context แบบ triggered |

#### การใช้งาน
```python
result = await service.retrieve(
    queries=[
        {"role": "user", "content": {"text": "ความชอบของเขาคืออะไร?"}},
        {"role": "user", "content": {"text": "บอกฉันเกี่ยวกับนิสัยการทำงาน"}}
    ],
    where={"user_id": "123"},  # Optional: กรอง scope
    method="rag"  # หรือ "llm" สำหรับการให้เหตุผลที่ลึกกว่า
)

# คืนค่าผลลัพธ์ที่รับรู้ context:
{
    "categories": [...],     # พื้นที่หัวข้อที่เกี่ยวข้อง
    "items": [...],          # ข้อเท็จจริงหน่วยความจำเฉพาะ
    "resources": [...],      # แหล่งข้อมูลต้นฉบับ
    "next_step_query": "..." # คาดการณ์ follow-up context
}
```

---

## 💡 ตัวอย่าง Proactive Scenarios

### ตัวอย่าง 1: ผู้ช่วยที่เรียนรู้อยู่เสมอ

เรียนรู้จากทุก interaction อัตโนมัติโดยไม่ต้องสั่งให้จำ:
```bash
export OPENAI_API_KEY=your_api_key
python examples/example_1_conversation_memory.py
```

**Proactive Behavior:**
- สกัดความชอบอัตโนมัติจากการพูดถึงแบบไม่เป็นทางการ
- สร้างโมเดลความสัมพันธ์จาก interaction patterns
- นำเสนอ context ที่เกี่ยวข้องในบทสนทนาในอนาคต

**เหมาะสำหรับ:** Personal AI assistants, customer support ที่จดจำได้, social chatbots

---

### ตัวอย่าง 2: Agent ที่ปรับปรุงตัวเอง

เรียนรู้จาก execution logs และแนะนำการปรับแต่งเชิงรุก:
```bash
export OPENAI_API_KEY=your_api_key
python examples/example_2_skill_extraction.py
```

**Proactive Behavior:**
- ติดตาม agent actions และผลลัพธ์อย่างต่อเนื่อง
- ระบุ patterns ในความสำเร็จและความล้มเหลว
- สร้าง skill guides อัตโนมัติจากประสบการณ์

**เหมาะสำหรับ:** DevOps automation, agent self-improvement, knowledge capture

---

### ตัวอย่าง 3: Multimodal Context Builder

รวมหน่วยความจำข้ามประเภท input ต่างๆ เพื่อสร้าง context ที่ครอบคลุม:
```bash
export OPENAI_API_KEY=your_api_key
python examples/example_3_multimodal_memory.py
```

**Proactive Behavior:**
- อ้างอิงข้าม text, images, และเอกสารอัตโนมัติ
- สร้างความเข้าใจรวมข้ามหลาย modalities
- นำเสนอ visual context เมื่อพูดถึงหัวข้อที่เกี่ยวข้อง

**เหมาะสำหรับ:** Documentation systems, learning platforms, research assistants

---

## 📊 ประสิทธิภาพ

memU ทำได้ **92.09% ความแม่นยำเฉลี่ย** บน Locomo benchmark ในทุก reasoning tasks แสดงให้เห็นการทำงาน proactive memory ที่เชื่อถือได้

<img width="100%" alt="benchmark" src="https://github.com/user-attachments/assets/6fec4884-94e5-4058-ad5c-baac3d7e76d9" />

ดูข้อมูลการทดลองโดยละเอียด: [memU-experiment](https://github.com/NevaMind-AI/memU-experiment)

---

## 🧩 Ecosystem

| Repository | คำอธิบาย | Proactive Features |
|------------|---------|-------------------|
| **[memU](https://github.com/NevaMind-AI/memU)** | Core proactive memory engine | 7×24 learning pipeline, auto-categorization |
| **[memU-server](https://github.com/NevaMind-AI/memU-server)** | Backend พร้อม continuous sync | Real-time memory updates, webhook triggers |
| **[memU-ui](https://github.com/NevaMind-AI/memU-ui)** | Visual memory dashboard | Live memory evolution monitoring |

**Quick Links:**
- 🚀 [ลอง MemU Cloud](https://app.memu.so/quick-start)
- 📚 [API Documentation](https://memu.pro/docs)
- 💬 [Discord Community](https://discord.gg/memu)

---

## 🤝 Partners

<div align="center">

<a href="https://github.com/TEN-framework/ten-framework"><img src="https://avatars.githubusercontent.com/u/113095513?s=200&v=4" alt="Ten" height="40" style="margin: 10px;"></a>
<a href="https://openagents.org"><img src="../assets/partners/openagents.png" alt="OpenAgents" height="40" style="margin: 10px;"></a>
<a href="https://github.com/milvus-io/milvus"><img src="https://miro.medium.com/v2/resize:fit:2400/1*-VEGyAgcIBD62XtZWavy8w.png" alt="Milvus" height="40" style="margin: 10px;"></a>

</div>

---

## 🤝 วิธีร่วมพัฒนา

เรายินดีรับการมีส่วนร่วมจากชุมชน! ไม่ว่าจะเป็นการแก้ bugs, เพิ่ม features, หรือปรับปรุงเอกสาร

### เริ่มต้น

#### ข้อกำหนดเบื้องต้น
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- Git

#### ตั้งค่า Development Environment
```bash
# 1. Fork และ clone repository
git clone https://github.com/YOUR_USERNAME/memU.git
cd memU

# 2. ติดตั้ง development dependencies
make install
```

คำสั่ง `make install` จะ:
- สร้าง virtual environment โดยใช้ `uv`
- ติดตั้ง project dependencies ทั้งหมด
- ตั้งค่า pre-commit hooks สำหรับการตรวจสอบคุณภาพโค้ด

#### รัน Quality Checks

ก่อน submit การมีส่วนร่วม ตรวจสอบว่าโค้ดผ่านการตรวจสอบทั้งหมด:
```bash
make check
```

---

## 📄 License

[Apache License 2.0](../LICENSE.txt)

---

## 🌍 ชุมชน

- **GitHub Issues**: [รายงาน bugs & ขอ features](https://github.com/NevaMind-AI/memU/issues)
- **Discord**: [เข้าร่วมชุมชน](https://discord.com/invite/hQZntfGsbJ)
- **X (Twitter)**: [ติดตาม @memU_ai](https://x.com/memU_ai)
- **ติดต่อ**: info@nevamind.ai

---

<div align="center">

⭐ **ให้ดาวเราบน GitHub** เพื่อรับการแจ้งเตือนเกี่ยวกับ releases ใหม่!

📚 **[คู่มือภาษาไทยฉบับสมบูรณ์](../docs/คู่มือ/README.md)**

</div>
