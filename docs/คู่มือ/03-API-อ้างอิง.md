[🏠 หน้าหลัก](../../README.md) | [📚 สารบัญ](README.md)

---

# บทที่ 3: API อ้างอิง

## `MemoryService` (หรือ `MemUService`)

### Constructor

```python
from memu.app import MemoryService

service = MemoryService(
    llm_profiles=...,        # จำเป็น: การตั้งค่า LLM providers
    database_config=...,     # Optional: การตั้งค่าฐานข้อมูล
    memorize_config=...,     # Optional: ปรับแต่งการสกัดหน่วยความจำ
    retrieve_config=...,     # Optional: ปรับแต่งการดึงหน่วยความจำ
)
```

### Parameters ทั้งหมด

| Parameter | Type | Default | คำอธิบาย |
|-----------|------|---------|---------|
| `llm_profiles` | `dict` | จำเป็น | ตั้งค่า LLM/embedding providers |
| `database_config` | `dict` | inmemory | ตั้งค่าฐานข้อมูล |
| `memorize_config` | `dict` | ค่าเริ่มต้น | ปรับแต่งการสกัด memory |
| `retrieve_config` | `dict` | ค่าเริ่มต้น | ปรับแต่งการดึง memory |

---

## `llm_profiles`

กำหนด LLM และ embedding providers ที่ใช้งาน

### OpenAI (ค่าเริ่มต้น)

```python
service = MemoryService(
    llm_profiles={
        "default": {
            "api_key": "sk-your-openai-key",
            "chat_model": "gpt-4o-mini",       # Optional, ค่าเริ่มต้น: gpt-4o-mini
            "embed_model": "text-embedding-3-small",  # Optional
        }
    }
)
```

### OpenRouter

```python
service = MemoryService(
    llm_profiles={
        "default": {
            "provider": "openrouter",
            "client_backend": "httpx",
            "base_url": "https://openrouter.ai",
            "api_key": "your-openrouter-key",
            "chat_model": "anthropic/claude-3.5-sonnet",
            "embed_model": "openai/text-embedding-3-small",
        }
    }
)
```

### Qwen (Alibaba DashScope)

```python
service = MemoryService(
    llm_profiles={
        "default": {
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "api_key": "your-dashscope-key",
            "chat_model": "qwen3-max",
            "client_backend": "sdk",  # ใช้ SDK แทน HTTP
        },
        # Profile แยกสำหรับ embeddings (Optional)
        "embedding": {
            "base_url": "https://api.voyageai.com/v1",
            "api_key": "your-voyage-key",
            "embed_model": "voyage-3.5-lite",
        }
    }
)
```

### Custom Provider

```python
service = MemoryService(
    llm_profiles={
        "default": {
            "base_url": "https://your-custom-api.com/v1",
            "api_key": "your-api-key",
            "chat_model": "your-model-name",
            "client_backend": "http",  # "sdk" หรือ "http" หรือ "httpx"
        }
    }
)
```

**`client_backend` options**:
- `"sdk"` — ใช้ OpenAI Python SDK (ค่าเริ่มต้น)
- `"http"` — ใช้ HTTP requests ตรง
- `"httpx"` — ใช้ httpx library (สำหรับ async)

---

## `database_config`

กำหนดว่าจะจัดเก็บหน่วยความจำที่ไหน

### In-Memory (สำหรับ testing)

```python
service = MemoryService(
    llm_profiles={"default": {"api_key": "..."}},
    database_config={
        "metadata_store": {"provider": "inmemory"},
    },
)
```

**ข้อดี**: ไม่ต้องติดตั้ง database, เริ่มใช้งานได้ทันที
**ข้อเสีย**: ข้อมูลหายเมื่อปิดโปรแกรม

---

### SQLite (สำหรับ local/portable)

```python
service = MemoryService(
    llm_profiles={"default": {"api_key": "..."}},
    database_config={
        "metadata_store": {
            "provider": "sqlite",
            "dsn": "sqlite:///my_memories.db",  # เส้นทางไฟล์
        },
    },
)
```

**DSN formats**:
- `sqlite:///memories.db` — relative path
- `sqlite:////home/user/memories.db` — absolute path (4 slashes)
- `sqlite:///:memory:` — in-memory SQLite

**Vector search**: ใช้ brute-force (รองรับถึง ~100k items)

---

### PostgreSQL + pgvector (สำหรับ production)

```python
service = MemoryService(
    llm_profiles={"default": {"api_key": "..."}},
    database_config={
        "metadata_store": {
            "provider": "postgres",
            "dsn": "postgresql://user:password@localhost:5432/memu",
        },
        "vector_index": {
            "provider": "pgvector",  # native vector search
        },
    },
)
```

ดูรายละเอียดการติดตั้ง PostgreSQL ใน [บทที่ 5](05-การติดตั้ง-PostgreSQL.md)

---

## `memorize()`

### Signature

```python
result = await service.memorize(
    resource_url: str,          # จำเป็น: เส้นทางไฟล์หรือ URL
    modality: str,              # จำเป็น: ประเภทของ resource
    user: dict | None = None,   # Optional: ขอบเขตผู้ใช้
)
```

### Parameters

| Parameter | Type | จำเป็น | คำอธิบาย |
|-----------|------|--------|---------|
| `resource_url` | `str` | ✅ | เส้นทางไฟล์ local หรือ URL |
| `modality` | `str` | ✅ | ประเภท: `conversation`, `document`, `image`, `video`, `audio` |
| `user` | `dict` | ❌ | ข้อมูลผู้ใช้เพื่อ scope หน่วยความจำ |

### Return Value

```python
{
    "resource": {
        "id": "uuid-string",
        "url": "path/to/file.json",
        "modality": "conversation",
        "created_at": "2024-01-01T00:00:00",
    },
    "items": [
        {
            "id": "uuid-string",
            "summary": "ผู้ใช้ชอบ dark mode",
            "memory_type": "preference",
            "embedding": [...],   # vector
        },
        # ... items อื่นๆ
    ],
    "categories": [
        {
            "id": "uuid-string",
            "name": "preferences",
            "description": "User preferences and settings",
            "summary": "ผู้ใช้ชอบ dark mode และ minimal UI...",
        },
        # ... categories อื่นๆ
    ]
}
```

### ตัวอย่าง: Conversation

```python
result = await service.memorize(
    resource_url="examples/resources/conversations/conv1.json",
    modality="conversation",
    user={"user_id": "alice"},
)

print(f"✅ สกัด {len(result['items'])} items")
print(f"✅ {len(result['categories'])} categories")
```

### ตัวอย่าง: Document

```python
result = await service.memorize(
    resource_url="examples/resources/docs/manual.txt",
    modality="document",
    user={"user_id": "alice", "agent_id": "support-bot"},
)
```

### ตัวอย่าง: Image

```python
result = await service.memorize(
    resource_url="examples/resources/images/diagram.png",
    modality="image",
    user={"user_id": "alice"},
)
```

---

## `retrieve()`

### Signature

```python
result = await service.retrieve(
    queries: list[dict],        # จำเป็น: รายการ queries
    where: dict | None = None,  # Optional: กรอง scope
    method: str = "rag",        # Optional: วิธีการดึง
)
```

### Parameters

| Parameter | Type | Default | คำอธิบาย |
|-----------|------|---------|---------|
| `queries` | `list[dict]` | จำเป็น | รายการ query messages |
| `where` | `dict` | `None` | กรอง user_id, agent_id |
| `method` | `str` | `"rag"` | วิธีการ: `"rag"` หรือ `"llm"` |

### `method="rag"` — Fast Context Assembly

ดึงข้อมูลด้วย embedding similarity:
- ⚡ เร็ว (sub-second)
- 💰 ถูก (เฉพาะ embedding cost)
- ✅ เหมาะสำหรับ real-time retrieval

### `method="llm"` — Deep Reasoning

ดึงข้อมูลด้วย LLM reasoning:
- 🧠 ฉลาดกว่า (เข้าใจ context ลึก)
- 🐢 ช้ากว่า (ต้องเรียก LLM)
- 💰💰 แพงกว่า
- ✅ เหมาะสำหรับ complex queries

### Queries Format

```python
queries = [
    # ประวัติบทสนทนา (ให้ context)
    {"role": "user", "content": {"text": "บอกฉันเกี่ยวกับความชอบ"}},
    {"role": "assistant", "content": {"text": "ได้เลย..."}},
    # Query ล่าสุด (ใช้ดึงหน่วยความจำ)
    {"role": "user", "content": {"text": "ความชอบของเขาคืออะไร?"}},
]
```

### `where` Filter

กำหนดขอบเขตของหน่วยความจำที่จะดึง:

```python
# เฉพาะผู้ใช้คนเดียว
where={"user_id": "alice"}

# เฉพาะ agents หลายตัว
where={"agent_id__in": ["bot-1", "bot-2"]}

# ไม่กำหนด where = ดึงทั้งหมด
where=None
```

### Return Value

```python
{
    "categories": [
        {
            "name": "preferences",
            "summary": "ผู้ใช้ชอบ dark mode...",
            "score": 0.92,
        }
    ],
    "items": [
        {
            "summary": "ผู้ใช้ชอบ dark mode",
            "memory_type": "preference",
            "score": 0.95,
        }
    ],
    "resources": [
        {
            "url": "conv1.json",
            "modality": "conversation",
        }
    ],
    "next_step_query": "ต้องการข้อมูลเพิ่มเติมเกี่ยวกับ UI preferences",
}
```

### ตัวอย่างการใช้งาน

```python
# RAG retrieval (เร็ว)
result = await service.retrieve(
    queries=[
        {"role": "user", "content": {"text": "Tell me about preferences"}},
        {"role": "assistant", "content": {"text": "Sure..."}},
        {"role": "user", "content": {"text": "What are they?"}},
    ],
    where={"user_id": "alice"},
    method="rag",
)

print("Categories:")
for cat in result.get("categories", [])[:3]:
    print(f"  📁 {cat['name']}: {cat.get('summary', '')[:60]}")

print("\nItems:")
for item in result.get("items", [])[:5]:
    print(f"  • {item.get('summary', '')}")
```

---

## `memorize_config`

ปรับแต่งวิธีที่ memU สกัดหน่วยความจำ:

```python
service = MemoryService(
    llm_profiles={"default": {"api_key": "..."}},
    memorize_config={
        # กำหนด memory types ที่ต้องการสกัด
        "memory_types": ["skill"],  # ค่าเริ่มต้น: ["fact", "preference", "skill"]

        # กำหนด prompt เฉพาะสำหรับแต่ละ type
        "memory_type_prompts": {
            "skill": """
                วิเคราะห์ log การทำงาน สกัด:
                1. Actions และ outcomes
                2. Root causes ของ failures
                3. Lessons learned
                Text: {resource}
            """
        },

        # กำหนด categories เอง (แทนที่ auto-generated)
        "memory_categories": [
            {
                "name": "deployment_execution",
                "description": "Deployment actions and results"
            },
            {
                "name": "lessons_learned",
                "description": "Key insights from experiences"
            },
        ],
    },
)
```

---

## `retrieve_config`

ปรับแต่งการดึงหน่วยความจำ:

```python
service = MemoryService(
    llm_profiles={"default": {"api_key": "..."}},
    retrieve_config={
        "method": "rag",   # ค่าเริ่มต้น: "rag"
        "top_k": 10,       # จำนวน items ที่ดึงมา
    },
)

# หรือเปลี่ยน method หลังสร้าง service
service.retrieve_config.method = "llm"
```

---

## ขั้นตอนถัดไป

- 📖 [บทที่ 4: ตัวอย่างจริง](04-ตัวอย่างจริง.md) — โค้ดตัวอย่างพร้อมใช้
- 📖 [บทที่ 5: PostgreSQL](05-การติดตั้ง-PostgreSQL.md) — ตั้งค่าฐานข้อมูล production
- 📖 [บทที่ 6: การผสานรวม](06-การผสานรวม.md) — เชื่อมต่อกับ LangGraph และ frameworks อื่น
