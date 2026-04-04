#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

default_msg() {
  printf 'chore: sync %s' "$(date -Iseconds 2>/dev/null || date '+%Y-%m-%dT%H:%M:%S%z')"
}

usage() {
  cat <<'EOF'
사용법:
  ./push.sh                         기본 메시지로 커밋 후 push
  ./push.sh "커밋 메시지"           지정 메시지로 커밋 후 push
  ./push.sh --push-only             커밋 없이 현재 브랜치만 push
  ./push.sh -h | --help             이 도움말
EOF
}

if [[ "${1:-}" == "--push-only" ]]; then
  git push
  exit 0
fi

if [[ "${1:-}" == "-h" ]] || [[ "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -eq 0 ]]; then
  MSG="$(default_msg)"
else
  MSG="$*"
fi
git add -A

if git diff --cached --quiet; then
  echo "커밋할 변경이 없습니다. push만 시도합니다."
else
  git commit -m "${MSG}"
fi

git push
