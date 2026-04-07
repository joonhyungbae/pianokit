#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WEB_DIR="${SCRIPT_DIR}/pianokit_web"
WEB_PORT="${WEB_PORT:-47653}"

if [[ ! -d "${WEB_DIR}" ]]; then
  echo "Error: '${WEB_DIR}' directory not found." >&2
  exit 1
fi

find_port_pids() {
  if command -v lsof >/dev/null 2>&1; then
    lsof -ti "tcp:${WEB_PORT}" -sTCP:LISTEN 2>/dev/null || true
    return
  fi

  if command -v ss >/dev/null 2>&1; then
    ss -ltnp "sport = :${WEB_PORT}" 2>/dev/null | sed -nE 's/.*pid=([0-9]+).*/\1/p' | sort -u
    return
  fi
}

PIDS="$(find_port_pids)"
if [[ -n "${PIDS}" ]]; then
  echo "Port ${WEB_PORT} is in use. Stopping existing process(es): ${PIDS}"
  kill ${PIDS} 2>/dev/null || true
  sleep 1

  REMAINING_PIDS="$(find_port_pids)"
  if [[ -n "${REMAINING_PIDS}" ]]; then
    echo "Force stopping remaining process(es): ${REMAINING_PIDS}"
    kill -9 ${REMAINING_PIDS} 2>/dev/null || true
  fi
fi

echo "Starting pianokit_web dev server on port ${WEB_PORT}"
cd "${WEB_DIR}"
npm run dev -- --host 0.0.0.0 --port "${WEB_PORT}" --strictPort
