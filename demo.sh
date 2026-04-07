#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

PIECE="${1:-satie}"
WS_PORT="${WS_PORT:-8766}"
WEB_PORT="${WEB_PORT:-43197}"
WEB_DIR="${SCRIPT_DIR}/pianokit_web"

# ── conda 활성화 ──────────────────────────────────────────────
set +u
eval "$(conda shell.bash hook)"
conda activate pianokit
set -u

# ── 필수 파일 확인 ────────────────────────────────────────────
declare -A SCORES=( [satie]="assets/scores/satie_gymnopedie.mid" )
declare -A AUDIOS=( [satie]="assets/satie_gymnopedie_no1.wav" )

if [[ -z "${SCORES[$PIECE]+x}" ]]; then
  echo "Error: 알 수 없는 곡 '${PIECE}'. 사용 가능: ${!SCORES[*]}" >&2
  exit 1
fi

for f in "${SCORES[$PIECE]}" "${AUDIOS[$PIECE]}"; do
  if [[ ! -f "$f" ]]; then
    echo "Error: 파일 없음 → $f" >&2
    exit 1
  fi
done

# ── 정리 함수 ─────────────────────────────────────────────────
PIDS=()
cleanup() {
  echo ""
  echo "⏹  데모 종료 중..."
  for pid in "${PIDS[@]}"; do
    kill "$pid" 2>/dev/null || true
  done
  wait 2>/dev/null || true
  echo "✅ 정리 완료"
}
trap cleanup EXIT INT TERM

# ── 1) 웹 dev 서버 (이미 떠 있으면 재사용) ───────────────────
web_already_running() {
  if command -v lsof >/dev/null 2>&1; then
    lsof -ti "tcp:${WEB_PORT}" -sTCP:LISTEN >/dev/null 2>&1 && return 0
  elif command -v ss >/dev/null 2>&1; then
    ss -ltn "sport = :${WEB_PORT}" 2>/dev/null | grep -q LISTEN && return 0
  fi
  return 1
}

if web_already_running; then
  echo "🌐 웹 서버가 이미 port ${WEB_PORT}에서 실행 중 — 재사용합니다."
elif [[ -d "${WEB_DIR}" ]]; then
  echo "🌐 웹 서버 시작 (port ${WEB_PORT})..."
  (cd "${WEB_DIR}" && npm run dev -- --host 0.0.0.0 --port "${WEB_PORT}" --strictPort) &
  PIDS+=($!)
  sleep 3
fi

# ── 2) matchmaker WebSocket 서버 (score following → /stage) ──
echo "📡 matchmaker 서버 시작 (port 8765)..."
python -m uvicorn server.main:app --host 0.0.0.0 --port 8765 &
PIDS+=($!)
sleep 1

# ── 3) 라이브 AI 반주 서버 ───────────────────────────────────
echo "🎹 라이브 AI 반주 시작 (piece=${PIECE}, ws=${WS_PORT})..."
echo ""
python server/accomp_server.py --piece "${PIECE}" --ws-port "${WS_PORT}" &
PIDS+=($!)

# ── 안내 ──────────────────────────────────────────────────────
echo ""
echo "============================================"
echo "  🎵 PianoKit 라이브 데모"
echo "============================================"
echo ""
echo "  웹사이트:   http://localhost:${WEB_PORT}"
echo "  /stage:     http://localhost:${WEB_PORT}/stage"
echo "  matchmaker: ws://localhost:8765/ws/follow"
echo "  AI 반주 WS: ws://localhost:${WS_PORT}"
echo ""
echo "  Ctrl+C 로 전체 종료"
echo "============================================"
echo ""

wait
