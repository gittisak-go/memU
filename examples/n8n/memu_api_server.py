"""
memU API Server สำหรับ N8N Integration

เซิร์ฟเวอร์ FastAPI ที่ให้ N8N เรียกใช้งาน memU ผ่าน HTTP API
รองรับทั้ง in-memory (สำหรับพัฒนา) และ PostgreSQL (สำหรับ production) ผ่าน DATABASE_URL

การใช้งาน:
    cp .env.example .env
    # แก้ไข .env ตามต้องการ
    uvicorn memu_api_server:app --host 0.0.0.0 --port 8001 --reload
"""

from __future__ import annotations

import contextlib
import logging
import os
import tempfile
import uuid
from typing import Any

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# โหลดค่าตัวแปรสภาพแวดล้อมจากไฟล์ .env
load_dotenv()

# ตั้งค่า logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("memu_api_server")

# --- โหลด MemoryService ---
from memu.app.service import MemoryService  # noqa: E402
from memu.app.settings import DatabaseConfig  # noqa: E402

# เลือก database backend ตาม DATABASE_URL
_database_url = os.getenv("DATABASE_URL")
_database_config: dict[str, Any]
if _database_url:
    # ใช้ PostgreSQL สำหรับ production
    _database_config = {
        "metadata_store": {"provider": "postgres", "connection_string": _database_url},
        "vector_index": {"provider": "postgres", "connection_string": _database_url},
    }
    logger.info("ใช้ PostgreSQL database: %s", _database_url.split("@")[-1])
else:
    # ใช้ in-memory สำหรับ development
    _database_config = {
        "metadata_store": {"provider": "in_memory"},
        "vector_index": {"provider": "in_memory"},
    }
    logger.info("ใช้ in-memory database (โหมดพัฒนา)")

# สร้าง MemoryService instance เดียวสำหรับทั้งแอป
_api_key = os.getenv("OPENAI_API_KEY", "")
if not _api_key:
    logger.warning("OPENAI_API_KEY ไม่ได้ถูกตั้งค่า — API calls จะล้มเหลวเมื่อมีการเรียกใช้ LLM")
memory_service = MemoryService(
    llm_profiles={
        "default": {
            "api_key": _api_key,
            "chat_model": "gpt-4o-mini",
        },
        "embedding": {
            "api_key": _api_key,
            "chat_model": "gpt-4o-mini",
            "embed_model": "text-embedding-3-small",
        },
    },
    database_config=_database_config,
)

# --- FastAPI App ---
app = FastAPI(
    title="memU API",
    description="HTTP API สำหรับเชื่อมต่อ memU กับ N8N",
    version="1.0.0",
)


# --- Request/Response Models ---
class MemorizeRequest(BaseModel):
    """คำขอบันทึกความทรงจำ"""

    user_id: str
    text: str
    modality: str = "conversation"


class RetrieveRequest(BaseModel):
    """คำขอค้นหาความทรงจำ"""

    user_id: str
    text: str


class HealthResponse(BaseModel):
    """สถานะของเซิร์ฟเวอร์"""

    status: str
    service: str


# --- Endpoints ---


@app.get("/health", response_model=HealthResponse, summary="ตรวจสอบสถานะเซิร์ฟเวอร์")
async def health_check() -> dict[str, str]:
    """ตรวจสอบว่าเซิร์ฟเวอร์ทำงานปกติหรือไม่"""
    return {"status": "ok", "service": "memU API"}


@app.post("/memorize", summary="บันทึกความทรงจำ")
async def memorize(request: MemorizeRequest) -> dict[str, Any]:
    """
    บันทึกข้อความลงใน memU สำหรับผู้ใช้ที่ระบุ

    - **user_id**: รหัสผู้ใช้
    - **text**: ข้อความที่ต้องการบันทึก
    - **modality**: ประเภทของข้อมูล (conversation, document, ฯลฯ)
    """
    logger.info("memorize: user_id=%s, modality=%s", request.user_id, request.modality)

    # เขียนข้อความลงไฟล์ชั่วคราว เพื่อส่งให้ memorize
    temp_filename = f"memu_n8n_{uuid.uuid4()}.txt"
    file_path = os.path.join(tempfile.gettempdir(), temp_filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(request.text)

        result = await memory_service.memorize(
            resource_url=file_path,
            modality=request.modality,
            user={"user_id": request.user_id},
        )
        logger.info("memorize สำเร็จ: user_id=%s, items=%d", request.user_id, len(result.get("items", [])))
        return {"status": "ok", "user_id": request.user_id, "items_count": len(result.get("items", []))}
    except Exception as e:
        logger.exception("memorize ล้มเหลว: user_id=%s", request.user_id)
        raise HTTPException(status_code=500, detail=str(e)) from e
    finally:
        with contextlib.suppress(OSError):
            os.remove(file_path)


@app.post("/retrieve", summary="ค้นหาความทรงจำ")
async def retrieve(request: RetrieveRequest) -> dict[str, Any]:
    """
    ค้นหาความทรงจำที่เกี่ยวข้องกับคำถามสำหรับผู้ใช้ที่ระบุ

    - **user_id**: รหัสผู้ใช้
    - **text**: ข้อความคำถามที่ใช้ค้นหา
    """
    logger.info("retrieve: user_id=%s, query='%s'", request.user_id, request.text[:50])

    try:
        queries = [{"role": "user", "content": request.text}]
        result = await memory_service.retrieve(
            queries=queries,
            where={"user_id": request.user_id},
        )
        items = result.get("items", [])
        logger.info("retrieve สำเร็จ: user_id=%s, items=%d", request.user_id, len(items))
        return {
            "status": "ok",
            "user_id": request.user_id,
            "items": items,
            "context": result.get("context", ""),
        }
    except Exception as e:
        logger.exception("retrieve ล้มเหลว: user_id=%s", request.user_id)
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/categories/{user_id}", summary="ดูหมวดหมู่ความทรงจำ")
async def get_categories(user_id: str) -> dict[str, Any]:
    """
    ดึงรายการหมวดหมู่ความทรงจำทั้งหมดของผู้ใช้

    - **user_id**: รหัสผู้ใช้
    """
    logger.info("get_categories: user_id=%s", user_id)

    try:
        result = await memory_service.list_memory_categories(where={"user_id": user_id})
        categories = result.get("categories", [])
        logger.info("get_categories สำเร็จ: user_id=%s, categories=%d", user_id, len(categories))
        return {
            "status": "ok",
            "user_id": user_id,
            "categories": categories,
        }
    except Exception as e:
        logger.exception("get_categories ล้มเหลว: user_id=%s", user_id)
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.delete("/memory/{user_id}", summary="ลบความทรงจำทั้งหมด")
async def delete_memory(user_id: str) -> dict[str, Any]:
    """
    ลบความทรงจำทั้งหมดของผู้ใช้

    - **user_id**: รหัสผู้ใช้
    """
    logger.info("delete_memory: user_id=%s", user_id)

    try:
        result = await memory_service.clear_memory(where={"user_id": user_id})
        logger.info("delete_memory สำเร็จ: user_id=%s", user_id)
        return {"status": "ok", "user_id": user_id, "deleted": result.get("deleted", 0)}
    except Exception as e:
        logger.exception("delete_memory ล้มเหลว: user_id=%s", user_id)
        raise HTTPException(status_code=500, detail=str(e)) from e


# --- Main ---
if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8001"))
    uvicorn.run("memu_api_server:app", host=host, port=port, reload=True)
