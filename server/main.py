"""
matchmaker WebSocket 서버 — /stage 라이브 추적 모드용.

사용법:
    uvicorn server.main:app --host 0.0.0.0 --port 8765

프론트엔드(/stage)가 WebSocket으로 연결하면:
  1. 클라이언트가 설정 JSON을 보냄 (score_file, performance_file 등)
  2. 서버가 matchmaker를 실행하고 beat position을 스트리밍
"""

from __future__ import annotations

import asyncio
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from queue import Queue, Empty

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="pianokit matchmaker server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("pianokit.server")
logging.basicConfig(level=logging.INFO)

executor = ThreadPoolExecutor(max_workers=2)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _run_matchmaker(config: dict, queue: Queue, stop_event: asyncio.Event):
    """matchmaker를 별도 스레드에서 실행하고 결과를 queue에 넣는다."""
    try:
        from matchmaker import Matchmaker

        score_file = str(PROJECT_ROOT / config["score_file"])

        kwargs = {
            "score_file": score_file,
            "input_type": config.get("input_type", "audio"),
        }

        if "performance_file" in config:
            kwargs["performance_file"] = str(
                PROJECT_ROOT / config["performance_file"]
            )

        if "device_name_or_index" in config:
            kwargs["device_name_or_index"] = config["device_name_or_index"]

        if "method" in config:
            kwargs["method"] = config["method"]

        mm = Matchmaker(**kwargs)

        for position in mm.run():
            if stop_event.is_set():
                break
            queue.put({"beat": float(position)})

        queue.put(None)  # sentinel
    except Exception as exc:
        logger.exception("matchmaker error")
        queue.put({"error": str(exc)})
        queue.put(None)


@app.websocket("/ws/follow")
async def follow(ws: WebSocket):
    await ws.accept()
    logger.info("WebSocket connected")

    try:
        raw = await ws.receive_text()
        config = json.loads(raw)
        logger.info("Config received: %s", config)
    except (WebSocketDisconnect, json.JSONDecodeError) as exc:
        logger.warning("Bad handshake: %s", exc)
        return

    queue: Queue = Queue()
    stop_event = asyncio.Event()
    loop = asyncio.get_event_loop()

    loop.run_in_executor(executor, _run_matchmaker, config, queue, stop_event)

    try:
        while True:
            try:
                msg = queue.get_nowait()
            except Empty:
                await asyncio.sleep(0.01)
                continue

            if msg is None:
                break
            await ws.send_json(msg)
    except WebSocketDisconnect:
        logger.info("Client disconnected")
        stop_event.set()
    finally:
        stop_event.set()

    try:
        await ws.close()
    except Exception:
        pass

    logger.info("Session ended")


@app.get("/health")
async def health():
    return {"status": "ok"}
