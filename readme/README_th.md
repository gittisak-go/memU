![MemU Banner](../assets/banner.png)

<div align="center">

# memU

### หน่วยความจำเชิงรุก 24/7 สำหรับ AI Agent

[![PyPI version](https://badge.fury.io/py/memu-py.svg)](https://badge.fury.io/py/memu-py)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Discord](https://img.shields.io/badge/Discord-Join%20Chat-5865F2?logo=discord&logoColor=white)](https://discord.gg/memu)
[![Twitter](https://img.shields.io/badge/Twitter-Follow-1DA1F2?logo=x&logoColor=white)](https://x.com/memU_ai)

<a href="https://trendshift.io/repositories/17374" target="_blank"><img src="https://trendshift.io/api/badge/repositories/17374" alt="NevaMind-AI%2FmemU | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

**[English](README_en.md) | [中文](README_zh.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Español](README_es.md) | [Français](README_fr.md) | [ภาษาไทย](README_th.md)**

</div>

---

memU คือเฟรมเวิร์กหน่วยความจำที่สร้างขึ้นสำหรับ **AI Agent แบบเชิงรุกที่ทำงาน 24/7**
ออกแบบมาเพื่อการใช้งานระยะยาว และ**ลดต้นทุน LLM token** ของการดูแล agent ให้ออนไลน์ตลอดเวลา
memU **จับและเข้าใจเจตนาของผู้ใช้อย่างต่อเนื่อง** แม้ไม่มีคำสั่ง agent ก็สามารถรู้ว่าคุณกำลังจะทำอะไรและลงมือทำเองได้

---

## 🤖 [ทางเลือกแทน OpenClaw (Moltbot, Clawdbot)](https://memu.bot)

<img width="100%" src="https://github.com/NevaMind-AI/memU/blob/main/assets/memUbot.png" />

- **ดาวน์โหลดและใช้งานได้ทันที** เริ่มต้นง่าย
- สร้างหน่วยความจำระยะยาวเพื่อ **เข้าใจเจตนาของผู้ใช้** และทำงานเชิงรุก
- **ลดต้นทุน LLM token** ด้วย context ที่กระชับขึ้น

ลองใช้เลย: [memU bot](https://memu.bot)

---

## 🗃️ หน่วยความจำแบบระบบไฟล์ ระบบไฟล์แบบหน่วยความจำ

memU จัดการ **หน่วยความจำเหมือนระบบไฟล์** — มีโครงสร้าง เป็นลำดับชั้น และเข้าถึงได้ทันที

| ระบบไฟล์ | หน่วยความจำ memU |
|-----------|-----------------|
| 📁 โฟลเดอร์ | 🏷️ หมวดหมู่ (หัวข้อที่จัดระเบียบอัตโนมัติ) |
| 📄 ไฟล์ | 🧠 รายการความจำ (ข้อเท็จจริง ความชอบ ทักษะที่ดึงออกมา) |
| 🔗 Symlinks | 🔄 อ้างอิงข้าม (ความจำที่เชื่อมโยงกัน) |
| 📂 Mount points | 📥 ทรัพยากร (บทสนทนา เอกสาร รูปภาพ) |

**ทำไมสิ่งนี้จึงสำคัญ:**
- **นำทางหน่วยความจำ** เหมือนการเรียกดูไดเรกทอรี — เจาะลึกจากหมวดหมู่กว้างไปยังข้อเท็จจริงเฉพาะเจาะจง
- **ติดตั้งความรู้ใหม่** ทันที — บทสนทนาและเอกสารกลายเป็นหน่วยความจำที่ค้นหาได้
- **เชื่อมโยงทุกอย่าง** — ความจำอ้างอิงถึงกัน สร้างกราฟความรู้ที่เชื่อมต่อกัน
- **คงทนและพกพาได้** — ส่งออก สำรอง และย้ายหน่วยความจำเหมือนไฟล์

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

เช่นเดียวกับที่ระบบไฟล์แปลง bytes ดิบให้เป็นข้อมูลที่จัดระเบียบ memU แปลงการโต้ตอบดิบให้เป็น **ปัญญาที่มีโครงสร้าง ค้นหาได้ และเชิงรุก**

---

## ⭐️ ให้ดาวกับ repository

<img width="100%" src="https://github.com/NevaMind-AI/memU/blob/main/assets/star.gif" />
หากคุณพบว่า memU มีประโยชน์หรือน่าสนใจ ดาว ⭐️ บน GitHub จะเป็นกำลังใจอย่างมาก

---

## ✨ ฟีเจอร์หลัก

| ความสามารถ | คำอธิบาย |
|------------|----------|
| 🤖 **Proactive Agent 24/7** | Memory agent ที่ทำงานต่อเนื่องในพื้นหลัง — ไม่เคยหลับ ไม่เคยลืม |
| 🎯 **จับเจตนาผู้ใช้** | เข้าใจและจดจำเป้าหมาย ความชอบ และ context ของผู้ใช้ข้ามเซสชันอัตโนมัติ |
| 💰 **ประหยัดต้นทุน** | ลดต้นทุน token ระยะยาวด้วยการ cache ข้อมูลเชิงลึกและหลีกเลี่ยงการเรียก LLM ซ้ำซ้อน |

---

## 🔄 วิธีที่หน่วยความจำเชิงรุกทำงาน

```bash

cd examples/proactive
python proactive.py

```

---

### วงจรชีวิตของหน่วยความจำเชิงรุก
```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                         USER QUERY                                               │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
                 │                                                           │
                 ▼                                                           ▼
┌────────────────────────────────────────┐         ┌────────────────────────────────────────────────┐
│         🤖 MAIN AGENT                  │         │              🧠 MEMU BOT                       │
│                                        │         │                                                │
│  Handle user queries & execute tasks   │  ◄───►  │  Monitor, memorize & proactive intelligence   │
├────────────────────────────────────────┤         ├────────────────────────────────────────────────┤
│                                        │         │                                                │
│  ┌──────────────────────────────────┐  │         │  ┌──────────────────────────────────────────┐  │
│  │  1. RECEIVE USER INPUT           │  │         │  │  1. MONITOR INPUT/OUTPUT                 │  │
│  │     Parse query, understand      │  │   ───►  │  │     Observe agent interactions           │  │
│  │     context and intent           │  │         │  │     Track conversation flow              │  │
│  └──────────────────────────────────┘  │         │  └──────────────────────────────────────────┘  │
│                 │                      │         │                    │                           │
│                 ▼                      │         │                    ▼                           │
│  ┌──────────────────────────────────┐  │         │  ┌──────────────────────────────────────────┐  │
│  │  2. PLAN & EXECUTE               │  │         │  │  2. MEMORIZE & EXTRACT                   │  │
│  │     Break down tasks             │  │   ◄───  │  │     Store insights, facts, preferences   │  │
│  │     Call tools, retrieve data    │  │  inject │  │     Extract skills & knowledge           │  │
│  │     Generate responses           │  │  memory │  │     Update user profile                  │  │
│  └──────────────────────────────────┘  │         │  └──────────────────────────────────────────┘  │
│                 │                      │         │                    │                           │
│                 ▼                      │         │                    ▼                           │
│  ┌──────────────────────────────────┐  │         │  ┌──────────────────────────────────────────┐  │
│  │  3. RESPOND TO USER              │  │         │  │  3. PREDICT USER INTENT                  │  │
│  │     Deliver answer/result        │  │   ───►  │  │     Anticipate next steps                │  │
│  │     Continue conversation        │  │         │  │     Identify upcoming needs              │  │
│  └──────────────────────────────────┘  │         │  └──────────────────────────────────────────┘  │
│                 │                      │         │                    │                           │
│                 ▼                      │         │                    ▼                           │
│  ┌──────────────────────────────────┐  │         │  ┌──────────────────────────────────────────┐  │
│  │  4. LOOP                         │  │         │  │  4. RUN PROACTIVE TASKS                  │  │
│  │     Wait for next user input     │  │   ◄───  │  │     Pre-fetch relevant context           │  │
│  │     or proactive suggestions     │  │  suggest│  │     Prepare recommendations              │  │
│  └──────────────────────────────────┘  │         │  │     Update todolist autonomously         │  │
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
Agent: "I found 3 new papers on RAG optimization that align with
        your recent research on retrieval systems. One author
        (Dr. Chen) you've cited before published yesterday."

# พฤติกรรมเชิงรุก:
- Learns topic preferences from browsing patterns
- Tracks author/source credibility preferences
- Filters noise based on engagement history
- Times recommendations for optimal attention
```

### 2. **จัดการอีเมล**
*Agent เรียนรู้รูปแบบการสื่อสารและจัดการการโต้ตอบประจำ*
```python
# MemU สังเกตรูปแบบอีเมลเมื่อเวลาผ่านไป:
- Response templates for common scenarios
- Priority contacts and urgent keywords
- Scheduling preferences and availability
- Writing style and tone variations

# การช่วยเหลืออีเมลเชิงรุก:
Agent: "You have 12 new emails. I've drafted responses for 3 routine
        requests and flagged 2 urgent items from your priority contacts.
        Should I also reschedule tomorrow's meeting based on the
        conflict John mentioned?"

# การทำงานอัตโนมัติ:
✓ Draft context-aware replies
✓ Categorize and prioritize inbox
✓ Detect scheduling conflicts
✓ Summarize long threads with key decisions
```

### 3. **ติดตามการซื้อขายและการเงิน**
*Agent ติดตาม context ตลาดและพฤติกรรมการลงทุนของผู้ใช้*
```python
# MemU เรียนรู้ความชอบในการซื้อขาย:
- Risk tolerance from historical decisions
- Preferred sectors and asset classes
- Response patterns to market events
- Portfolio rebalancing triggers

# การแจ้งเตือนเชิงรุก:
Agent: "NVDA dropped 5% in after-hours trading. Based on your past
        behavior, you typically buy tech dips above 3%. Your current
        allocation allows for $2,000 additional exposure while
        maintaining your 70/30 equity-bond target."

# การติดตามต่อเนื่อง:
- Track price alerts tied to user-defined thresholds
- Correlate news events with portfolio impact
- Learn from executed vs. ignored recommendations
- Anticipate tax-loss harvesting opportunities
```

...

---

## 🗂️ สถาปัตยกรรมหน่วยความจำแบบลำดับชั้น

ระบบสามชั้นของ MemU รองรับทั้ง **การสืบค้นแบบ reactive** และ **การโหลด context เชิงรุก**:

<img width="100%" alt="structure" src="../assets/structure.png" />

| ชั้น | การใช้งาน Reactive | การใช้งาน Proactive |
|------|-------------------|---------------------|
| **Resource** | เข้าถึงข้อมูลต้นฉบับโดยตรง | ติดตามพื้นหลังเพื่อหารูปแบบใหม่ |
| **Item** | ดึงข้อเท็จจริงที่เฉพาะเจาะจง | การดึงข้อมูลแบบ real-time จากการโต้ตอบที่กำลังดำเนินอยู่ |
| **Category** | ภาพรวมระดับสรุป | การประกอบ context อัตโนมัติสำหรับการคาดการณ์ |

**ประโยชน์เชิงรุก:**
- **Auto-categorization**: ความจำใหม่จัดระเบียบตัวเองเป็นหัวข้อ
- **Pattern Detection**: ระบบระบุธีมที่เกิดซ้ำ
- **Context Prediction**: คาดการณ์ว่าจะต้องการข้อมูลใดต่อไป

---

## 🚀 เริ่มต้นอย่างรวดเร็ว

### ตัวเลือก 1: Cloud Version

สัมผัสประสบการณ์หน่วยความจำเชิงรุกทันที:

👉 **[memu.so](https://memu.so)** - บริการ hosted พร้อมการเรียนรู้ต่อเนื่อง 7×24

สำหรับการ deploy ระดับองค์กรพร้อม proactive workflows แบบกำหนดเอง ติดต่อ **info@nevamind.ai**

#### Cloud API (v3)

| Base URL | `https://api.memu.so` |
|----------|----------------------|
| Auth | `Authorization: Bearer YOUR_API_KEY` |

| Method | Endpoint | คำอธิบาย |
|--------|----------|----------|
| `POST` | `/api/v3/memory/memorize` | ลงทะเบียนงานการเรียนรู้ต่อเนื่อง |
| `GET` | `/api/v3/memory/memorize/status/{task_id}` | ตรวจสอบสถานะการประมวลผลแบบ real-time |
| `POST` | `/api/v3/memory/categories` | รายการหมวดหมู่ที่สร้างอัตโนมัติ |
| `POST` | `/api/v3/memory/retrieve` | สืบค้นหน่วยความจำ (รองรับการโหลด context เชิงรุก) |

📚 **[เอกสาร API เต็มรูปแบบ](https://memu.pro/docs#cloud-version)**

---

### ตัวเลือก 2: Self-Hosted

#### การติดตั้ง
```bash
pip install -e .
```

#### ตัวอย่างพื้นฐาน

> **ข้อกำหนด**: Python 3.13+ และ OpenAI API key

**ทดสอบการเรียนรู้ต่อเนื่อง** (in-memory):
```bash
export OPENAI_API_KEY=your_api_key
cd tests
python test_inmemory.py
```

**ทดสอบด้วย Persistent Storage** (PostgreSQL):
```bash
# เริ่ม PostgreSQL พร้อม pgvector
docker run -d \
  --name memu-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=memu \
  -p 5432:5432 \
  pgvector/pgvector:pg16

# รันการทดสอบการเรียนรู้ต่อเนื่อง
export OPENAI_API_KEY=your_api_key
cd tests
python test_postgres.py
```

ตัวอย่างทั้งสองแสดง **proactive memory workflows**:
1. **Continuous Ingestion**: ประมวลผลไฟล์หลายไฟล์ตามลำดับ
2. **Auto-Extraction**: การสร้างหน่วยความจำทันที
3. **Proactive Retrieval**: การนำเสนอหน่วยความจำตาม context

ดู [`tests/test_inmemory.py`](../tests/test_inmemory.py) และ [`tests/test_postgres.py`](../tests/test_postgres.py) สำหรับรายละเอียดการใช้งาน

---

### Custom LLM และผู้ให้บริการ Embedding

MemU รองรับผู้ให้บริการ LLM และ embedding แบบกำหนดเองนอกเหนือจาก OpenAI กำหนดค่าผ่าน `llm_profiles`:
```python
from memu import MemUService

service = MemUService(
    llm_profiles={
        # Default profile for LLM operations
        "default": {
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "api_key": "your_api_key",
            "chat_model": "qwen3-max",
            "client_backend": "sdk"  # "sdk" or "http"
        },
        # Separate profile for embeddings
        "embedding": {
            "base_url": "https://api.voyageai.com/v1",
            "api_key": "your_voyage_api_key",
            "embed_model": "voyage-3.5-lite"
        }
    },
    # ... other configuration
)
```

---

### การผสานรวม OpenRouter

MemU รองรับ [OpenRouter](https://openrouter.ai) เป็นผู้ให้บริการ model ช่วยให้คุณเข้าถึงผู้ให้บริการ LLM หลายรายผ่าน API เดียว

#### การกำหนดค่า
```python
from memu import MemoryService

service = MemoryService(
    llm_profiles={
        "default": {
            "provider": "openrouter",
            "client_backend": "httpx",
            "base_url": "https://openrouter.ai",
            "api_key": "your_openrouter_api_key",
            "chat_model": "anthropic/claude-3.5-sonnet",  # Any OpenRouter model
            "embed_model": "openai/text-embedding-3-small",  # Embedding model
        },
    },
    database_config={
        "metadata_store": {"provider": "inmemory"},
    },
)
```

#### Environment Variables

| Variable | คำอธิบาย |
|----------|----------|
| `OPENROUTER_API_KEY` | OpenRouter API key จาก [openrouter.ai/keys](https://openrouter.ai/keys) |

#### ฟีเจอร์ที่รองรับ

| ฟีเจอร์ | สถานะ | หมายเหตุ |
|---------|-------|---------|
| Chat Completions | รองรับ | ทำงานกับ OpenRouter chat model ทุกตัว |
| Embeddings | รองรับ | ใช้ OpenAI embedding models ผ่าน OpenRouter |
| Vision | รองรับ | ใช้ vision-capable models (เช่น `openai/gpt-4o`) |

#### การรัน OpenRouter Tests
```bash
export OPENROUTER_API_KEY=your_api_key

# Full workflow test (memorize + retrieve)
python tests/test_openrouter.py

# Embedding-specific tests
python tests/test_openrouter_embedding.py

# Vision-specific tests
python tests/test_openrouter_vision.py
```

ดู [`examples/example_4_openrouter_memory.py`](../examples/example_4_openrouter_memory.py) สำหรับตัวอย่างที่ใช้งานได้จริง

---

## 📖 Core APIs

### `memorize()` - Continuous Learning Pipeline

ประมวลผล input แบบ real-time และอัปเดตหน่วยความจำทันที:

<img width="100%" alt="memorize" src="../assets/memorize.png" />

```python
result = await service.memorize(
    resource_url="path/to/file.json",  # File path or URL
    modality="conversation",            # conversation | document | image | video | audio
    user={"user_id": "123"}             # Optional: scope to a user
)

# Returns immediately with extracted memory:
{
    "resource": {...},      # Stored resource metadata
    "items": [...],         # Extracted memory items (available instantly)
    "categories": [...]     # Auto-updated category structure
}
```

**ฟีเจอร์เชิงรุก:**
- การประมวลผลแบบ Zero-delay — หน่วยความจำพร้อมใช้งานทันที
- การจัดหมวดหมู่อัตโนมัติโดยไม่ต้องติดแท็กด้วยตนเอง
- อ้างอิงข้ามกับหน่วยความจำที่มีอยู่เพื่อตรวจหารูปแบบ

### `retrieve()` - Dual-Mode Intelligence

MemU รองรับทั้ง **การโหลด context เชิงรุก** และ **การสืบค้นแบบ reactive**:

<img width="100%" alt="retrieve" src="../assets/retrieve.png" />

#### RAG-based Retrieval (`method="rag"`)

การประกอบ **context เชิงรุก** อย่างรวดเร็วโดยใช้ embeddings:

- ✅ **Context ทันที**: การนำเสนอหน่วยความจำต่ำกว่าวินาที
- ✅ **การติดตามพื้นหลัง**: สามารถรันต่อเนื่องโดยไม่มีต้นทุน LLM
- ✅ **การให้คะแนนความคล้ายคลึง**: ระบุหน่วยความจำที่เกี่ยวข้องมากที่สุดอัตโนมัติ

#### LLM-based Retrieval (`method="llm"`)

**การใช้เหตุผลเชิงคาดการณ์** อย่างลึกซึ้งสำหรับ context ที่ซับซ้อน:

- ✅ **การทำนายเจตนา**: LLM อนุมานสิ่งที่ผู้ใช้ต้องการก่อนที่จะถาม
- ✅ **การพัฒนาการสืบค้น**: ปรับปรุงการค้นหาอัตโนมัติตาม context ที่พัฒนา
- ✅ **การยุติเร็ว**: หยุดเมื่อรวบรวม context เพียงพอ

#### การเปรียบเทียบ

| แง่มุม | RAG (Context เร็ว) | LLM (การใช้เหตุผลลึก) |
|--------|-------------------|----------------------|
| **ความเร็ว** | ⚡ มิลลิวินาที | 🐢 วินาที |
| **ต้นทุน** | 💰 Embedding เท่านั้น | 💰💰 LLM inference |
| **การใช้งานเชิงรุก** | การติดตามต่อเนื่อง | การโหลด context ที่กระตุ้นแล้ว |
| **เหมาะสำหรับ** | การแนะนำแบบ real-time | การคาดการณ์ที่ซับซ้อน |

#### การใช้งาน
```python
# Proactive retrieval with context history
result = await service.retrieve(
    queries=[
        {"role": "user", "content": {"text": "What are their preferences?"}},
        {"role": "user", "content": {"text": "Tell me about work habits"}}
    ],
    where={"user_id": "123"},  # Optional: scope filter
    method="rag"  # or "llm" for deeper reasoning
)

# Returns context-aware results:
{
    "categories": [...],     # Relevant topic areas (auto-prioritized)
    "items": [...],          # Specific memory facts
    "resources": [...],      # Original sources for traceability
    "next_step_query": "..." # Predicted follow-up context
}
```

**การกรองเชิงรุก**: ใช้ `where` เพื่อกำหนดขอบเขตการติดตามต่อเนื่อง:
- `where={"user_id": "123"}` - Context เฉพาะผู้ใช้
- `where={"agent_id__in": ["1", "2"]}` - การประสานงานหลาย agent
- ละเว้น `where` สำหรับการตระหนักรู้ context ระดับโลก

---

## 📊 ประสิทธิภาพ

MemU บรรลุ **ความแม่นยำเฉลี่ย 92.09%** บน Locomo benchmark ในงานการใช้เหตุผลทั้งหมด แสดงให้เห็นการดำเนินการ proactive memory ที่เชื่อถือได้

<img width="100%" alt="benchmark" src="https://github.com/user-attachments/assets/6fec4884-94e5-4058-ad5c-baac3d7e76d9" />

ดูข้อมูลการทดลองโดยละเอียด: [memU-experiment](https://github.com/NevaMind-AI/memU-experiment)

---

## 🧩 Ecosystem

| Repository | คำอธิบาย | ฟีเจอร์เชิงรุก |
|------------|----------|---------------|
| **[memU](https://github.com/NevaMind-AI/memU)** | Core proactive memory engine | 7×24 learning pipeline, auto-categorization |
| **[memU-server](https://github.com/NevaMind-AI/memU-server)** | Backend พร้อม continuous sync | Real-time memory updates, webhook triggers |
| **[memU-ui](https://github.com/NevaMind-AI/memU-ui)** | Visual memory dashboard | Live memory evolution monitoring |

**Quick Links:**
- 🚀 [ลอง MemU Cloud](https://app.memu.so/quick-start)
- 📚 [เอกสาร API](https://memu.pro/docs)
- 💬 [Discord Community](https://discord.gg/memu)

---

## 🌱 memU เพื่อสังคมไทย

AI ที่ดีไม่ควรอยู่แค่ในบริษัทเทคโนโลยี
มันควรอยู่ในโรงเรียนชนบท ในมือของ อสม.
ในกลุ่มออมทรัพย์หมู่บ้าน และในทุกครอบครัวที่ดูแลผู้สูงวัย

| กรณีการใช้งาน | ช่วยใคร | สิ่งที่ memU จำ |
|--------------|---------|----------------|
| 🏫 **ผู้ช่วยครู** | ครูและนักเรียน | จุดแข็ง จุดอ่อน คะแนนของนักเรียนแต่ละคน |
| 👴 **ดูแลผู้สูงอายุ** | ผู้สูงอายุและครอบครัว | ยา นัดหมาย อาการ |
| 🏠 **ผู้ช่วยครอบครัว** | ครอบครัว | ตารางเวลา วันเกิด รายการสิ่งที่ต้องทำ |
| 🌾 **เศรษฐกิจชุมชน** | หมู่บ้านและกลุ่ม OTOP | รายได้ ค่าใช้จ่าย สมาชิก สินค้าคงคลัง |
| 🤝 **ป้องกันยาเสพติด** | อาสาสมัครชุมชน (อสม.) | ทรัพยากร กิจกรรม ผลลัพธ์ (privacy-first) |

ดูตัวอย่างการใช้งานเพื่อชุมชนไทย: [examples/community/](../examples/community/)

---

## 🤝 พาร์ทเนอร์

<div align="center">

<a href="https://github.com/TEN-framework/ten-framework"><img src="https://avatars.githubusercontent.com/u/113095513?s=200&v=4" alt="Ten" height="40" style="margin: 10px;"></a>
<a href="https://openagents.org"><img src="../assets/partners/openagents.png" alt="OpenAgents" height="40" style="margin: 10px;"></a>
<a href="https://github.com/milvus-io/milvus"><img src="https://miro.medium.com/v2/resize:fit:2400/1*-VEGyAgcIBD62XtZWavy8w.png" alt="Milvus" height="40" style="margin: 10px;"></a>
<a href="https://xroute.ai/"><img src="../assets/partners/xroute.png" alt="xRoute" height="40" style="margin: 10px;"></a>
<a href="https://jaaz.app/"><img src="../assets/partners/jazz.png" alt="Jazz" height="40" style="margin: 10px;"></a>
<a href="https://github.com/Buddie-AI/Buddie"><img src="../assets/partners/buddie.png" alt="Buddie" height="40" style="margin: 10px;"></a>
<a href="https://github.com/bytebase/bytebase"><img src="../assets/partners/bytebase.png" alt="Bytebase" height="40" style="margin: 10px;"></a>
<a href="https://github.com/LazyAGI/LazyLLM"><img src="../assets/partners/LazyLLM.png" alt="LazyLLM" height="40" style="margin: 10px;"></a>

</div>

---

## 🤝 วิธีการมีส่วนร่วม

เรายินดีรับการมีส่วนร่วมจากชุมชน! ไม่ว่าจะเป็นการแก้ไขบั๊ก เพิ่มฟีเจอร์ หรือปรับปรุงเอกสาร ความช่วยเหลือของคุณเป็นที่ชื่นชม

### การเริ่มต้น

เพื่อเริ่มมีส่วนร่วมกับ MemU คุณจะต้องตั้งค่าสภาพแวดล้อมการพัฒนา:

#### ข้อกำหนดเบื้องต้น
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- Git

#### ตั้งค่าสภาพแวดล้อมการพัฒนา
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

#### การรัน Quality Checks

ก่อนส่ง contribution ตรวจสอบให้แน่ใจว่าโค้ดผ่านการตรวจสอบคุณภาพทั้งหมด:
```bash
make check
```

คำสั่ง `make check` รัน:
- **Lock file verification**: ตรวจสอบความสอดคล้องของ `pyproject.toml`
- **Pre-commit hooks**: Lint โค้ดด้วย Ruff, format ด้วย Black
- **Type checking**: รัน `mypy` สำหรับการวิเคราะห์ type แบบ static
- **Dependency analysis**: ใช้ `deptry` เพื่อค้นหา dependencies ที่ล้าสมัย

### แนวทางการมีส่วนร่วม

สำหรับแนวทางการมีส่วนร่วมโดยละเอียด มาตรฐานโค้ด และแนวปฏิบัติการพัฒนา โปรดดู [CONTRIBUTING.md](../CONTRIBUTING.md)

**เคล็ดลับด่วน:**
- สร้าง branch ใหม่สำหรับแต่ละฟีเจอร์หรือการแก้ไขบั๊ก
- เขียน commit messages ที่ชัดเจน
- เพิ่ม tests สำหรับฟังก์ชันการทำงานใหม่
- อัปเดตเอกสารตามที่จำเป็น
- รัน `make check` ก่อน push

---

## 📄 ใบอนุญาต

[Apache License 2.0](../LICENSE.txt)

---

## 🌍 ชุมชน

- **GitHub Issues**: [รายงานบั๊กและขอฟีเจอร์](https://github.com/NevaMind-AI/memU/issues)
- **Discord**: [เข้าร่วมชุมชน](https://discord.com/invite/hQZntfGsbJ)
- **X (Twitter)**: [ติดตาม @memU_ai](https://x.com/memU_ai)
- **ติดต่อ**: info@nevamind.ai

---

<div align="center">

⭐ **ให้ดาวเราบน GitHub** เพื่อรับการแจ้งเตือนเกี่ยวกับการเปิดตัวใหม่!

</div>
