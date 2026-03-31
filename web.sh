#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WEB_DIR="${SCRIPT_DIR}/pianokit_web"
WEB_PORT="${WEB_PORT:-43197}"

if [[ ! -d "${WEB_DIR}" ]]; then
  echo "Error: '${WEB_DIR}' directory not found." >&2
  exit 1
fi

echo "Starting pianokit_web dev server on port ${WEB_PORT}"
cd "${WEB_DIR}"
npm run dev -- --host 0.0.0.0 --port "${WEB_PORT}" --strictPort
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WEB_DIR="${SCRIPT_DIR}/pianokit_web"

if [[ ! -d "${WEB_DIR}" ]]; then
  echo "Error: '${WEB_DIR}' directory not found." >&2
  exit 1
fi

echo "Deploying pianokit_web from ${WEB_DIR}"
cd "${WEB_DIR}"
npm run deploy
