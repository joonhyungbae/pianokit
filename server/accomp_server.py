#!/usr/bin/env python3
"""
라이브 AI 반주자 데모 — matchmaker + FluidSynth

실행:
    conda activate pianokit
    python server/accomp_server.py [--piece satie]

하는 일:
    1. Satie 녹음을 스피커로 재생
    2. 동시에 matchmaker가 악보 위치를 실시간 추적
    3. 추적된 위치에 따라 반주 음표를 FluidSynth로 실시간 합성
    4. WebSocket(ws://localhost:8766)으로 /stage에 beat position 전송
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import threading
import time
from pathlib import Path
from queue import Queue, Empty

import numpy as np
import pretty_midi
import sounddevice as sd
import librosa

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")
logger = logging.getLogger("accomp")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SF2_PATH = "/usr/share/sounds/sf2/FluidR3_GM.sf2"

PIECES = {
    "satie": {
        "title": "Satie — Gymnopédie No.1",
        "score": "assets/scores/satie_gymnopedie.mid",
        "audio": "assets/satie_gymnopedie_no1.wav",
    },
}


def load_accompaniment(score_path: str) -> list[dict]:
    """악보에서 반주(왼손) 음표를 로드한다."""
    midi = pretty_midi.PrettyMIDI(str(PROJECT_ROOT / score_path))
    if len(midi.instruments) < 2:
        raise ValueError("악보에 2개 이상의 트랙이 필요합니다 (멜로디+반주)")
    accomp = midi.instruments[1]
    notes = []
    for n in accomp.notes:
        notes.append({
            "pitch": n.pitch,
            "velocity": n.velocity,
            "start_beat": n.start,
            "end_beat": n.end,
        })
    notes.sort(key=lambda x: x["start_beat"])
    return notes


def run_matchmaker_thread(
    score_path: str,
    audio_path: str,
    beat_queue: Queue,
    stop_event: threading.Event,
):
    """matchmaker를 별도 스레드에서 실행, beat 위치를 큐에 넣는다."""
    try:
        from matchmaker import Matchmaker

        mm = Matchmaker(
            score_file=str(PROJECT_ROOT / score_path),
            performance_file=str(PROJECT_ROOT / audio_path),
            input_type="audio",
        )
        frame_rate = mm.frame_rate
        beat_queue.put(("meta", {"frame_rate": frame_rate}))

        for pos in mm.run():
            if stop_event.is_set():
                break
            beat_queue.put(("beat", float(pos)))

        beat_queue.put(("done", None))
    except Exception as exc:
        logger.exception("matchmaker error")
        beat_queue.put(("error", str(exc)))


def play_audio_thread(
    audio_path: str,
    sr: int,
    start_event: threading.Event,
    stop_event: threading.Event,
):
    """오디오 파일을 스피커로 재생한다."""
    audio, _ = librosa.load(str(PROJECT_ROOT / audio_path), sr=sr, mono=True)
    logger.info("Audio loaded: %.1fs at %dHz", len(audio) / sr, sr)

    start_event.wait()
    if stop_event.is_set():
        return

    logger.info("▶ Playing audio...")
    try:
        sd.play(audio, samplerate=sr)
        sd.wait()
    except Exception as exc:
        logger.error("Audio playback error: %s", exc)
    logger.info("⏹ Audio playback finished")


def accompany_thread(
    notes: list[dict],
    beat_queue: Queue,
    ws_queue: Queue,
    start_event: threading.Event,
    stop_event: threading.Event,
):
    """matchmaker beat에 따라 FluidSynth로 반주를 실시간 합성한다."""
    import fluidsynth

    fs = fluidsynth.Synth()
    fs.start(driver="pulseaudio")
    sfid = fs.sfload(SF2_PATH)
    fs.program_select(0, sfid, 0, 0)
    fs.setting("synth.gain", 0.6)
    logger.info("FluidSynth ready (pulseaudio)")

    frame_rate = None
    frame_idx = 0
    active_notes: set[int] = set()
    next_note_idx = 0
    last_beat = 0.0

    start_event.wait()
    t0 = time.monotonic()

    while not stop_event.is_set():
        try:
            msg_type, payload = beat_queue.get(timeout=0.5)
        except Empty:
            continue

        if msg_type == "meta":
            frame_rate = payload["frame_rate"]
            logger.info("Frame rate: %s", frame_rate)
            continue
        elif msg_type in ("done", "error"):
            if msg_type == "error":
                logger.error("matchmaker: %s", payload)
            break
        elif msg_type == "beat":
            current_beat = payload
        else:
            continue

        frame_idx += 1
        if frame_rate:
            expected_time = frame_idx / frame_rate
            elapsed = time.monotonic() - t0
            if elapsed < expected_time:
                time.sleep(expected_time - elapsed)

        ws_queue.put({"beat": current_beat, "time": time.monotonic() - t0})

        # Note-on: 새로운 반주 음표 트리거
        while next_note_idx < len(notes):
            n = notes[next_note_idx]
            if n["start_beat"] <= current_beat:
                if n["pitch"] not in active_notes:
                    fs.noteon(0, n["pitch"], n["velocity"])
                    active_notes.add(n["pitch"])
                next_note_idx += 1
            else:
                break

        # Note-off: 끝난 음표 해제
        ended = set()
        for pitch in active_notes:
            for n in notes:
                if n["pitch"] == pitch and n["end_beat"] <= current_beat:
                    ended.add(pitch)
                    break
        for pitch in ended:
            fs.noteoff(0, pitch)
            active_notes.discard(pitch)

        last_beat = current_beat

    for pitch in active_notes:
        fs.noteoff(0, pitch)

    fs.delete()
    logger.info("FluidSynth stopped")


async def ws_server(ws_queue: Queue, host: str, port: int, stop_event: threading.Event):
    """WebSocket 서버 — /stage 페이지에 beat position을 스트리밍한다."""
    clients: set = set()

    async def handler(reader, writer):
        pass

    import websockets

    async def ws_handler(websocket):
        clients.add(websocket)
        logger.info("WS client connected (%d total)", len(clients))
        try:
            async for _ in websocket:
                pass
        except websockets.ConnectionClosed:
            pass
        finally:
            clients.discard(websocket)
            logger.info("WS client disconnected (%d total)", len(clients))

    server = await websockets.serve(ws_handler, host, port)
    logger.info("WebSocket server on ws://%s:%d", host, port)

    while not stop_event.is_set():
        try:
            msg = ws_queue.get_nowait()
            data = json.dumps(msg)
            if clients:
                await asyncio.gather(
                    *[c.send(data) for c in clients],
                    return_exceptions=True,
                )
        except Empty:
            pass
        await asyncio.sleep(0.01)

    server.close()
    await server.wait_closed()


def main():
    parser = argparse.ArgumentParser(description="라이브 AI 반주자 데모")
    parser.add_argument("--piece", default="satie", choices=list(PIECES.keys()))
    parser.add_argument("--ws-port", type=int, default=8766)
    parser.add_argument("--sr", type=int, default=44100)
    args = parser.parse_args()

    piece = PIECES[args.piece]
    logger.info("=== 라이브 AI 반주자: %s ===", piece["title"])

    notes = load_accompaniment(piece["score"])
    logger.info("Accompaniment: %d notes", len(notes))

    beat_queue: Queue = Queue()
    ws_queue: Queue = Queue()
    stop_event = threading.Event()
    start_event = threading.Event()

    # matchmaker 스레드 (미리 시작 — 로딩에 시간이 걸림)
    mm_thread = threading.Thread(
        target=run_matchmaker_thread,
        args=(piece["score"], piece["audio"], beat_queue, stop_event),
        daemon=True,
    )

    # 오디오 재생 스레드
    audio_thread = threading.Thread(
        target=play_audio_thread,
        args=(piece["audio"], args.sr, start_event, stop_event),
        daemon=True,
    )

    # 반주 스레드
    accomp_thread = threading.Thread(
        target=accompany_thread,
        args=(notes, beat_queue, ws_queue, start_event, stop_event),
        daemon=True,
    )

    mm_thread.start()
    audio_thread.start()
    accomp_thread.start()

    logger.info("Threads started. Press Enter to begin, Ctrl+C to quit.")
    try:
        input()
    except (KeyboardInterrupt, EOFError):
        stop_event.set()
        return

    start_event.set()
    logger.info("▶ Demo started!")

    # WebSocket 서버 실행 (메인 스레드)
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(ws_server(ws_queue, "0.0.0.0", args.ws_port, stop_event))
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        stop_event.set()
    finally:
        loop.close()

    mm_thread.join(timeout=5)
    audio_thread.join(timeout=5)
    accomp_thread.join(timeout=5)
    logger.info("=== Done ===")


if __name__ == "__main__":
    main()
