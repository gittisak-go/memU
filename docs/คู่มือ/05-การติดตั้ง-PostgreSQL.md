[🏠 หน้าหลัก](../../README.md) | [📚 สารบัญ](README.md)

---

# บทที่ 5: การติดตั้ง PostgreSQL + pgvector

## ทำไมต้องใช้ PostgreSQL + pgvector?

| ด้าน | SQLite | PostgreSQL + pgvector |
|-----|--------|----------------------|
| การตั้งค่า | ไม่ต้องตั้งค่า | ต้องตั้งค่า server |
| Concurrent access | Single writer | Full concurrent access |
| Vector search | Brute-force | Native pgvector index |
| ขนาดข้อมูล | ~100k items | หลาย millions items |
| Production | ❌ ไม่แนะนำ | ✅ แนะนำ |

**เหมาะสำหรับ production เมื่อ**:
- มีผู้ใช้หลายคนพร้อมกัน
- มีหน่วยความจำมากกว่า 100,000 items
- ต้องการ vector search ที่เร็วและ scalable
- ต้องการ full-text search ประสิทธิภาพสูง

---

## ติดตั้งด้วย Docker (แนะนำ)

### ติดตั้ง Docker

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose

# macOS
brew install --cask docker

# Windows: ดาวน์โหลดจาก https://www.docker.com/products/docker-desktop
```

### รัน PostgreSQL + pgvector

```bash
docker run -d \
  --name memu-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=memu \
  -p 5432:5432 \
  pgvector/pgvector:pg16
```

ตรวจสอบว่ารันอยู่:
```bash
docker ps
# ต้องเห็น memu-postgres ในรายการ
```

### ด้วย Docker Compose

สร้างไฟล์ `docker-compose.yml`:

```yaml
version: "3.8"

services:
  postgres:
    image: pgvector/pgvector:pg16
    container_name: memu-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: memu
    ports:
      - "5432:5432"
    volumes:
      - memu_pgdata:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  memu_pgdata:
```

รัน:
```bash
docker-compose up -d
```

---

## ติดตั้งบน Ubuntu/Debian (ไม่ใช้ Docker)

```bash
# 1. ติดตั้ง PostgreSQL
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib

# 2. ติดตั้ง pgvector
sudo apt-get install -y postgresql-16-pgvector

# 3. เริ่ม PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# 4. สร้าง database
sudo -u postgres psql -c "CREATE DATABASE memu;"
sudo -u postgres psql -c "CREATE USER memu_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE memu TO memu_user;"

# 5. เปิดใช้งาน pgvector extension
sudo -u postgres psql -d memu -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

---

## ติดตั้งบน macOS

```bash
# ติดตั้ง PostgreSQL ด้วย Homebrew
brew install postgresql@16
brew services start postgresql@16

# ติดตั้ง pgvector
brew install pgvector

# สร้าง database
createdb memu
psql memu -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

---

## ติดตั้งบน Windows

1. ดาวน์โหลด PostgreSQL จาก [postgresql.org](https://www.postgresql.org/download/windows/)
2. รัน installer และตั้งค่า:
   - Port: 5432
   - Password: ตามต้องการ
3. ติดตั้ง pgvector:
   ```cmd
   # ใน pgAdmin SQL Tool
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

---

## ติดตั้ง memU dependencies สำหรับ PostgreSQL

```bash
# ติดตั้ง postgres extras
pip install "memu-py[postgres]"

# หรือด้วย uv
uv add "memu-py[postgres]"

# หรือจาก source
pip install -e ".[postgres]"
```

---

## ตั้งค่า `database_config` ใน Python

### การเชื่อมต่อพื้นฐาน

```python
from memu.app import MemoryService

service = MemoryService(
    llm_profiles={
        "default": {
            "api_key": "your-openai-key",
            "chat_model": "gpt-4o-mini",
        }
    },
    database_config={
        "metadata_store": {
            "provider": "postgres",
            "dsn": "postgresql://postgres:postgres@localhost:5432/memu",
        },
    },
)
```

### DSN Format

```
postgresql://[user]:[password]@[host]:[port]/[database]

# ตัวอย่าง:
postgresql://postgres:mypassword@localhost:5432/memu
postgresql://memu_user:secret@db.example.com:5432/production_db
```

### ใช้ Environment Variable

```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/memu"
```

```python
import os

service = MemoryService(
    llm_profiles={"default": {"api_key": os.getenv("OPENAI_API_KEY")}},
    database_config={
        "metadata_store": {
            "provider": "postgres",
            "dsn": os.getenv("DATABASE_URL"),
        },
    },
)
```

---

## ทดสอบการเชื่อมต่อ

```bash
export OPENAI_API_KEY=your_api_key
cd tests
python test_postgres.py
```

ผลลัพธ์ที่คาดหวัง:
```
[POSTGRES] Starting test...
[POSTGRES] Memorizing...
  - preferences: ผู้ใช้ชอบ dark mode...
[POSTGRES] RETRIEVED - RAG
  Categories:
    - preferences: ...
  Items:
    ...
```

---

## Migration: SQLite → PostgreSQL

ถ้ามีข้อมูลใน SQLite อยู่แล้วและต้องการย้ายไป PostgreSQL:

```python
import json
from memu.database.sqlite import build_sqlite_database
from memu.database.postgres import build_postgres_database
from memu.app.settings import DatabaseConfig
from pydantic import BaseModel


class UserScope(BaseModel):
    user_id: str


# โหลดจาก SQLite
sqlite_config = DatabaseConfig(
    metadata_store={"provider": "sqlite", "dsn": "sqlite:///memu.db"}
)
sqlite_db = build_sqlite_database(config=sqlite_config, user_model=UserScope)
sqlite_db.load_existing()

# เชื่อมต่อ PostgreSQL
postgres_config = DatabaseConfig(
    metadata_store={
        "provider": "postgres",
        "dsn": "postgresql://postgres:postgres@localhost:5432/memu"
    }
)
postgres_db = build_postgres_database(config=postgres_config, user_model=UserScope)

# Migrate resources
for res_id, resource in sqlite_db.resources.items():
    postgres_db.resource_repo.create_resource(
        url=resource.url,
        modality=resource.modality,
        local_path=resource.local_path,
        caption=resource.caption,
        embedding=resource.embedding,
        user_data={"user_id": getattr(resource, "user_id", None)},
    )

print("✅ Migration เสร็จสมบูรณ์!")
```

---

## Performance Tips

### 1. Connection Pooling

```python
# ใช้ connection pool สำหรับ production
database_config={
    "metadata_store": {
        "provider": "postgres",
        "dsn": "postgresql://postgres:postgres@localhost:5432/memu",
        "pool_size": 10,        # จำนวน connections ใน pool
        "max_overflow": 20,     # connections เพิ่มเติมชั่วคราว
    },
}
```

### 2. Vector Index

pgvector รองรับหลาย index types:

```sql
-- HNSW index (เร็วกว่า, แนะนำสำหรับ production)
CREATE INDEX ON memory_items USING hnsw (embedding vector_cosine_ops);

-- IVFFlat index (ประหยัด memory กว่า)
CREATE INDEX ON memory_items USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
```

### 3. ตั้งค่า PostgreSQL สำหรับ Vector Workload

เพิ่มใน `postgresql.conf`:
```
# เพิ่ม shared memory
shared_buffers = 256MB

# เพิ่ม work memory สำหรับ vector operations
work_mem = 64MB

# เปิด parallel query
max_parallel_workers_per_gather = 4
```

### 4. Monitoring

```sql
-- ตรวจสอบขนาดตาราง
SELECT
    relname,
    pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- ตรวจสอบ index usage
SELECT indexrelname, idx_scan
FROM pg_stat_user_indexes
WHERE relname = 'memory_items';
```

---

## Troubleshooting

### ❌ `Connection refused to localhost:5432`

PostgreSQL ไม่ได้รัน:
```bash
# Docker
docker start memu-postgres

# Ubuntu service
sudo systemctl start postgresql
```

### ❌ `extension "vector" does not exist`

pgvector ยังไม่ได้ install:
```bash
# Docker: ใช้ image pgvector/pgvector แทน postgres
docker run ... pgvector/pgvector:pg16

# Ubuntu
sudo apt-get install postgresql-16-pgvector
```

### ❌ `password authentication failed`

```bash
# Reset password
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'new_password';"
```

### ❌ Slow vector search

```sql
-- ตรวจสอบว่ามี index
\d memory_items

-- สร้าง index ถ้ายังไม่มี
CREATE INDEX ON memory_items USING hnsw (embedding vector_cosine_ops);
```

---

## ขั้นตอนถัดไป

- 📖 [บทที่ 6: การผสานรวม](06-การผสานรวม.md) — เชื่อมต่อกับ LangGraph และ frameworks อื่น
