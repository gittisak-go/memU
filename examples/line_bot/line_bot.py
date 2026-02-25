"""
LINE Bot Integration for memU

วิธีใช้งาน:
    cp .env.example .env
    # แก้ไขค่า environment variables ใน .env
    uvicorn line_bot:app --host 0.0.0.0 --port 8000
"""

import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from linebot.v3 import WebhookParser
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from memu.app.service import MemoryService

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── LINE SDK setup ────────────────────────────────────────────────────────────
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(LINE_CHANNEL_SECRET)

# ── memU setup ────────────────────────────────────────────────────────────────
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

service = MemoryService(
    llm_profiles={
        "default": {
            "api_key": OPENAI_API_KEY,
            "chat_model": "gpt-4o-mini",
        },
    },
)

app = FastAPI(title="memU LINE Bot")


# ── helpers ───────────────────────────────────────────────────────────────────

async def _memorize(user_id: str, text: str) -> None:
    """บันทึกข้อความของผู้ใช้เข้า memU"""
    try:
        await service.memorize(
            resource_url=text,
            modality="conversation",
            user={"user_id": user_id},
        )
    except Exception:
        logger.exception("memorize failed for user %s", user_id)


async def _retrieve(user_id: str, text: str) -> str:
    """ดึงความจำที่เกี่ยวข้องกับข้อความ แล้วคืนเป็น string สรุป"""
    try:
        result = await service.retrieve(
            queries=[{"role": "user", "content": {"text": text}}],
            where={"user_id": user_id},
        )
        items = result.get("items", [])
        if not items:
            return ""
        snippets = [
            item.get("content", "") or item.get("text", "")
            for item in items[:5]
            if isinstance(item, dict)
        ]
        return "\n".join(s for s in snippets if s)
    except Exception:
        logger.exception("retrieve failed for user %s", user_id)
        return ""


async def _build_reply(user_id: str, user_text: str) -> str:
    """สร้างคำตอบโดยใช้ความจำจาก memU เป็น context"""
    memory_context = await _retrieve(user_id, user_text)

    system_prompt = (
        "คุณคือผู้ช่วย AI ที่มีหน่วยความจำระยะยาว "
        "ตอบภาษาไทยหรือภาษาเดียวกับที่ผู้ใช้พูด"
    )
    if memory_context:
        system_prompt += f"\n\nความทรงจำที่เกี่ยวข้อง:\n{memory_context}"

    llm = service.llm_client
    response = await llm.chat(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ]
    )
    return response.strip() if isinstance(response, str) else str(response)


# ── webhook endpoint ──────────────────────────────────────────────────────────

@app.post("/callback")
async def callback(request: Request) -> dict:
    """LINE Webhook endpoint — รับ event จาก LINE Platform"""
    signature = request.headers.get("X-Line-Signature", "")
    body = await request.body()

    try:
        events = parser.parse(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        logger.warning("Invalid LINE signature")
        raise HTTPException(status_code=400, detail="Invalid signature")

    async with AsyncApiClient(configuration) as api_client:
        line_bot_api = AsyncMessagingApi(api_client)

        for event in events:
            if not isinstance(event, MessageEvent):
                continue
            if not isinstance(event.message, TextMessageContent):
                continue

            user_id: str = event.source.user_id
            user_text: str = event.message.text
            reply_token: str = event.reply_token

            logger.info("Message from %s: %s", user_id, user_text)

            # 1. บันทึกข้อความผู้ใช้เข้า memU
            await _memorize(user_id, user_text)

            # 2. สร้างคำตอบโดยใช้ความจำเป็น context
            reply_text = await _build_reply(user_id, user_text)

            # 3. ส่งคำตอบกลับ LINE
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[TextMessage(text=reply_text)],
                )
            )

    return {"status": "ok"}


@app.get("/health")
async def health() -> dict:
    return {"status": "healthy"}
