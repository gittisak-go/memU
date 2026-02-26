"""
memU API Server for N8N Integration
====================================
FastAPI server that exposes memU as an HTTP API for N8N workflow automation.

Usage:
    pip install -r requirements.txt
    cp .env.example .env  # fill in your credentials
    uvicorn memu_api_server:app --host 0.0.0.0 --port 8000 --reload

Endpoints:
    POST /memorize    - Store a memory for a user
    POST /retrieve    - Retrieve memories relevant to a query
    GET  /health      - Health check
    GET  /categories  - List memory categories for a user
    DELETE /memory    - Clear all memories for a user
"""

from __future__ import annotations

import json
import logging
import os
import tempfile
from typing import Any

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="memU API for N8N",
    description="HTTP API ที่ให้ N8N เรียกใช้ memU สำหรับสร้าง AI Agent ที่มีหน่วยความจำระยะยาว",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------

def _get_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY", "")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set. Please configure your .env file.")
    return key


def _build_service() -> Any:
    """Build a MemoryService instance from environment variables."""
    from memu.app import MemoryService

    api_key = _get_api_key()
    chat_model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
    embed_model = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
    database_url = os.getenv("DATABASE_URL")

    database_config: dict[str, Any] = {}
    if database_url:
        database_config = {
            "metadata_store": {"provider": "sqlite", "dsn": database_url}
            if database_url.startswith("sqlite")
            else {"provider": "postgres", "dsn": database_url},
        }

    return MemoryService(
        llm_profiles={
            "default": {
                "api_key": api_key,
                "chat_model": chat_model,
                "embed_model": embed_model,
            },
        },
        database_config=database_config if database_config else None,
    )


# Lazy singleton — created once on first request
_service: Any = None


def _get_service() -> Any:
    global _service  # noqa: PLW0603
    if _service is None:
        _service = _build_service()
    return _service


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------


class MemorizeRequest(BaseModel):
    user_id: str = Field(..., description="Unique user identifier (e.g. LINE UID)")
    text: str = Field(..., description="Text content to memorize")
    modality: str = Field(default="conversation", description="Input modality: conversation, document, etc.")


class RetrieveRequest(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    text: str = Field(..., description="Query text to search memories")
    modality: str = Field(default="conversation", description="(reserved for future use)")


class DeleteMemoryRequest(BaseModel):
    user_id: str = Field(..., description="Unique user identifier whose memories will be cleared")


class CategoriesRequest(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")


# ---------------------------------------------------------------------------
# Helper: write text to a temp conversation JSON file
# ---------------------------------------------------------------------------


def _write_conversation_resource(text: str) -> str:
    """
    Serialize a plain-text message into the conversation JSON format that
    memU's memorize() pipeline expects, then write it to a temp file.

    Returns the absolute path of the temp file.
    """
    payload = {
        "content": [
            {
                "role": "user",
                "content": {"text": text},
                "created_at": "",
            }
        ]
    }
    tmp = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False,
        encoding="utf-8",
    )
    json.dump(payload, tmp, ensure_ascii=False)
    tmp.close()
    return tmp.name


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.get("/health", summary="Health check")
async def health() -> dict[str, str]:
    """ตรวจสอบว่า API Server ทำงานอยู่"""
    return {"status": "ok", "service": "memU API for N8N"}


@app.post("/memorize", summary="บันทึกความจำ")
async def memorize(req: MemorizeRequest) -> JSONResponse:
    """
    รับข้อความจาก N8N แล้วบันทึกลง memU memory store
    ใช้ modality='conversation' สำหรับข้อความสนทนา
    """
    service = _get_service()
    resource_path = _write_conversation_resource(req.text)
    try:
        result = await service.memorize(
            resource_url=resource_path,
            modality=req.modality,
            user={"user_id": req.user_id},
        )
    except Exception as exc:
        logger.exception("memorize failed for user=%s", req.user_id)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        try:
            os.unlink(resource_path)
        except OSError:
            pass

    return JSONResponse(content={"success": True, "user_id": req.user_id, "result": result})


@app.post("/retrieve", summary="ดึงความจำ")
async def retrieve(req: RetrieveRequest) -> JSONResponse:
    """
    รับ query จาก N8N แล้วค้นหาความจำที่เกี่ยวข้องใน memU
    คืนค่า items ที่เกี่ยวข้องและ context สำหรับส่งต่อให้ OpenAI/LLM node
    """
    service = _get_service()
    try:
        result = await service.retrieve(
            queries=[{"role": "user", "content": req.text}],
            where={"user_id": req.user_id},
        )
    except Exception as exc:
        logger.exception("retrieve failed for user=%s", req.user_id)
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    # Build a single context string that LLM nodes can inject into their system prompt
    items = result.get("items", [])
    context_parts = [item.get("summary", "") for item in items if item.get("summary")]
    memory_context = "\n".join(f"- {p}" for p in context_parts) if context_parts else ""

    return JSONResponse(
        content={
            "success": True,
            "user_id": req.user_id,
            "memory_context": memory_context,
            "items": items,
            "raw": result,
        }
    )


@app.get("/categories", summary="ดูหมวดหมู่ความจำ")
async def list_categories(user_id: str) -> JSONResponse:
    """
    ดึงรายการ memory categories ทั้งหมดของ user
    ใช้สำหรับ memory_dashboard workflow
    """
    service = _get_service()
    try:
        result = await service.list_memory_categories(where={"user_id": user_id})
    except Exception as exc:
        logger.exception("list_categories failed for user=%s", user_id)
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return JSONResponse(content={"success": True, "user_id": user_id, "categories": result.get("categories", [])})


@app.delete("/memory", summary="ลบความจำ")
async def delete_memory(req: DeleteMemoryRequest) -> JSONResponse:
    """
    ลบความจำทั้งหมดของ user ที่ระบุ
    """
    service = _get_service()
    try:
        result = await service.clear_memory(where={"user_id": req.user_id})
    except Exception as exc:
        logger.exception("clear_memory failed for user=%s", req.user_id)
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return JSONResponse(content={"success": True, "user_id": req.user_id, "cleared": result})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    uvicorn.run("memu_api_server:app", host=host, port=port, reload=False)
