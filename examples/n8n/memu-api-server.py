"""
memU API Server สำหรับ N8N Integration

FastAPI server ที่ N8N เรียกผ่าน HTTP Node ได้:
  POST /memorize     — บันทึกความจำ
  POST /retrieve     — ดึงความจำ
  GET  /health       — health check
  GET  /categories   — ดูหมวดหมู่ความจำ (ต้องระบุ user_id ใน query string)
  DELETE /memory     — ลบความจำของ user

Usage:
    cp .env.example .env
    # แก้ไข OPENAI_API_KEY ใน .env
    pip install -r requirements.txt
    uvicorn memu-api-server:app --host 0.0.0.0 --port 8001
"""

from __future__ import annotations

import logging
import os
import tempfile
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="memU API for N8N",
    description="HTTP API server เชื่อม memU กับ N8N workflow automation",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# MemoryService initialisation (lazy, shared across requests)
# ---------------------------------------------------------------------------

_service: Any = None


def _get_service() -> Any:
    global _service  # noqa: PLW0603
    if _service is not None:
        return _service

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Please configure it in the .env file.")

    from memu.app import MemoryService

    database_config: dict[str, Any] = {}
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        database_config = {
            "metadata_store": {"provider": "postgresql", "url": database_url},
        }

    _service = MemoryService(
        llm_profiles={
            "default": {
                "api_key": api_key,
                "chat_model": "gpt-4o-mini",
            },
        },
        database_config=database_config if database_config else None,
    )
    logger.info("MemoryService initialised")
    return _service


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------


class MemorizeRequest(BaseModel):
    user_id: str
    text: str
    modality: str = "conversation"


class RetrieveRequest(BaseModel):
    user_id: str
    text: str
    modality: str = "conversation"


class DeleteRequest(BaseModel):
    user_id: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "memU API for N8N"}


@app.post("/memorize")
async def memorize(req: MemorizeRequest) -> dict[str, Any]:
    """
    บันทึกความจำจาก N8N.

    รับ JSON:
    {
      "user_id": "line_uid_xxx",
      "text": "ข้อความที่ต้องการบันทึก",
      "modality": "conversation"
    }
    """
    service = _get_service()

    # เขียน text ลงไฟล์ชั่วคราวเพื่อส่งให้ MemoryService
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as tmp:
        tmp.write(req.text)
        tmp_path = tmp.name

    try:
        result = await service.memorize(
            resource_url=tmp_path,
            modality=req.modality,
            user={"user_id": req.user_id},
        )
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

    return {
        "status": "ok",
        "user_id": req.user_id,
        "items_stored": len(result.get("items", [])),
        "categories": len(result.get("categories", [])),
    }


@app.post("/retrieve")
async def retrieve(req: RetrieveRequest) -> dict[str, Any]:
    """
    ดึงความจำที่เกี่ยวข้องจาก N8N.

    รับ JSON:
    {
      "user_id": "line_uid_xxx",
      "text": "คำถามหรือบริบทที่ต้องการค้นหา",
      "modality": "conversation"
    }
    """
    service = _get_service()

    result = await service.retrieve(
        queries=[{"role": "user", "content": req.text}],
        where={"user_id": req.user_id},
    )

    memories = result.get("memories", [])
    summary = result.get("summary", "")

    return {
        "status": "ok",
        "user_id": req.user_id,
        "summary": summary,
        "memories": memories,
        "count": len(memories),
    }


@app.get("/categories")
async def categories(user_id: str = Query(..., description="LINE user ID")) -> dict[str, Any]:
    """
    ดูหมวดหมู่ความจำของ user.

    Query parameter: user_id=line_uid_xxx
    """
    service = _get_service()

    result = await service.list_memory_categories(
        where={"user_id": user_id},
    )

    return {
        "status": "ok",
        "user_id": user_id,
        "categories": result.get("categories", []),
    }


@app.delete("/memory")
async def delete_memory(req: DeleteRequest) -> dict[str, Any]:
    """
    ลบความจำทั้งหมดของ user.

    รับ JSON:
    {
      "user_id": "line_uid_xxx"
    }
    """
    service = _get_service()

    await service.clear_memory(
        where={"user_id": req.user_id},
    )

    return {
        "status": "ok",
        "user_id": req.user_id,
        "message": f"ลบความจำของ {req.user_id} เรียบร้อยแล้ว",
    }
